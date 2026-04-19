import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


FORBIDDEN_MARKERS = [
    "content_volume:",
    "给下游排版器",
    "这里建议分栏",
    "TODO",
    "系统提示词",
]
SINGLE_PAGE_LAYOUTS = {
    "Single-Page No Photo",
    "Single-Page With Photo",
}


def normalize_layout_mode(layout_mode: str, multi_page_variant: str) -> tuple[str, str]:
    if layout_mode == "Single-Page No Photo":
        return "Single-Page No Photo", "not_required"
    if layout_mode == "Single-Page With Photo":
        return "Single-Page With Photo", "not_required"
    if layout_mode == "Multi-Page With Photo":
        return "Multi-Page With Photo", "With Photo"
    if layout_mode == "Multi-Page No Photo":
        return "Multi-Page No Photo", "No Photo"

    if layout_mode == "Single-Page Extreme":
        return "Single-Page No Photo", "not_required"
    if layout_mode == "Single-Page Photo":
        return "Single-Page With Photo", "not_required"
    if layout_mode == "Multi-Page Comfortable":
        if multi_page_variant == "With Photo":
            return "Multi-Page With Photo", "With Photo"
        if multi_page_variant == "No Photo":
            return "Multi-Page No Photo", "No Photo"

    return layout_mode, multi_page_variant


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def count_pdf_pages(path: Path) -> int:
    data = path.read_bytes()
    text = data.decode("latin-1", errors="ignore")
    return len(re.findall(r"/Type\s*/Page\b", text))


def add_check(checks: list[dict], name: str, passed: bool, detail: str) -> None:
    checks.append({"name": name, "passed": passed, "detail": detail})


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Stage 3 outputs against the Stage 2 handoff manifest.")
    parser.add_argument("--output-dir", required=True, help="Directory containing the resume artifacts")
    parser.add_argument(
        "--manifest",
        default=None,
        help="Optional explicit path to resume_pipeline_handoff.json",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir).resolve()
    manifest_path = Path(args.manifest).resolve() if args.manifest else output_dir / "resume_pipeline_handoff.json"
    checks = []
    failures = []
    warnings = []

    manifest_exists = manifest_path.is_file()
    add_check(checks, "manifest_exists", manifest_exists, str(manifest_path))
    if not manifest_exists:
        failures.append("Missing resume_pipeline_handoff.json")
        result = {
            "valid": False,
            "checks": checks,
            "warnings": warnings,
            "failures": failures,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    raw_path = output_dir / manifest.get("stage1", {}).get("artifact", "raw_content.md")
    refined_path = output_dir / manifest.get("stage2", {}).get("artifact", "refined_resume.md")
    html_path = output_dir / manifest.get("stage3", {}).get("artifact_html", "index.html")
    pdf_path = output_dir / manifest.get("stage3", {}).get("artifact_pdf", manifest.get("pdf_name", "output_resume.pdf"))
    layout_mode, _ = normalize_layout_mode(
        manifest.get("layout_mode"),
        manifest.get("multi_page_variant", "not_required"),
    )
    expected_refined_sha = manifest.get("stage3", {}).get("expected_refined_resume_sha256")

    for name, path in [
        ("raw_content_exists", raw_path),
        ("refined_resume_exists", refined_path),
        ("index_html_exists", html_path),
        ("output_pdf_exists", pdf_path),
    ]:
        exists = path.is_file()
        add_check(checks, name, exists, str(path))
        if not exists:
            failures.append(f"Missing required artifact: {path.name}")

    if failures:
        result = {
            "valid": False,
            "checks": checks,
            "warnings": warnings,
            "failures": failures,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    refined_sha = sha256_file(refined_path)
    refined_unchanged = refined_sha == expected_refined_sha
    add_check(
        checks,
        "refined_resume_unchanged_since_stage2",
        refined_unchanged,
        f"expected={expected_refined_sha}, current={refined_sha}",
    )
    if not refined_unchanged:
        failures.append("Stage 3 changed refined_resume.md after Stage 2 handoff")

    html_text = html_path.read_text(encoding="utf-8", errors="replace")
    html_required_markers = [
        "<html",
        ".a4-page",
        "section-content",
    ]
    missing_html_markers = [marker for marker in html_required_markers if marker not in html_text]
    add_check(
        checks,
        "html_contains_required_structure_markers",
        not missing_html_markers,
        "none missing" if not missing_html_markers else ", ".join(missing_html_markers),
    )
    if missing_html_markers:
        failures.append("index.html is missing required structure markers")

    html_forbidden_hits = [marker for marker in FORBIDDEN_MARKERS if marker in html_text]
    add_check(
        checks,
        "html_has_no_process_marker_leaks",
        not html_forbidden_hits,
        "none found" if not html_forbidden_hits else ", ".join(html_forbidden_hits),
    )
    if html_forbidden_hits:
        failures.append("Process markers leaked into index.html")

    pdf_size_ok = pdf_path.stat().st_size > 0
    add_check(checks, "pdf_non_empty", pdf_size_ok, str(pdf_path.stat().st_size))
    if not pdf_size_ok:
        failures.append("Generated PDF is empty")

    page_count = count_pdf_pages(pdf_path)
    single_page_ok = True
    if layout_mode in SINGLE_PAGE_LAYOUTS:
        single_page_ok = page_count == 1
        add_check(checks, "single_page_pdf_has_one_page", single_page_ok, str(page_count))
        if not single_page_ok:
            failures.append(f"Single-page output has {page_count} pages")
    else:
        add_check(checks, "pdf_has_at_least_one_page", page_count >= 1, str(page_count))
        if page_count < 1:
            failures.append("PDF page count could not be detected")

    result = {
        "valid": not failures,
        "checks": checks,
        "warnings": warnings,
        "failures": failures,
        "page_count": page_count,
        "layout_mode": layout_mode,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
