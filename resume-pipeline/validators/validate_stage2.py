import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


NARRATIVE_TITLES = {
    "工作经历",
    "项目经历",
    "实习经历",
    "校园经历",
    "Work Experience",
    "Projects",
    "Internship Experience",
    "Extracurricular Activities",
}

DATA_TITLES = {
    "专业技能",
    "荣誉奖项",
    "科研成果",
    "证书资质",
    "语言能力",
    "Skills",
    "Honors & Awards",
    "Publications",
    "Certifications",
    "Languages",
}

EDUCATION_TITLES = {"教育背景", "Education"}

FORBIDDEN_MARKERS = [
    "content_volume:",
    "给下游排版器",
    "这里建议分栏",
    "TODO",
    "系统提示词",
]

FORBIDDEN_SECTION_TITLES = {
    "个人总结",
    "Summary",
}

SECTION_RE = re.compile(r"^##\s+(.+?)(?:\s+<!--\s*type:\s*(narrative|data)\s*-->)?\s*$")
CANONICAL_LAYOUT_CHOICES = [
    "Single-Page No Photo",
    "Single-Page With Photo",
    "Multi-Page With Photo",
    "Multi-Page No Photo",
]
LEGACY_LAYOUT_CHOICES = [
    "Single-Page Extreme",
    "Single-Page Photo",
    "Multi-Page Comfortable",
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


def parse_sections(text: str) -> list[dict]:
    sections = []
    for line in text.splitlines():
        match = SECTION_RE.match(line.strip())
        if match:
            sections.append({"title": match.group(1).strip(), "type": match.group(2)})
    return sections


def add_check(checks: list[dict], name: str, passed: bool, detail: str) -> None:
    checks.append({"name": name, "passed": passed, "detail": detail})


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Stage 2 outputs and write a handoff manifest.")
    parser.add_argument("--output-dir", required=True, help="Directory containing raw_content.md and refined_resume.md")
    parser.add_argument(
        "--layout-mode",
        required=True,
        choices=CANONICAL_LAYOUT_CHOICES + LEGACY_LAYOUT_CHOICES,
        help="Layout mode selected for the workflow",
    )
    parser.add_argument(
        "--multi-page-variant",
        choices=["With Photo", "No Photo", "not_required"],
        default="not_required",
        help="Optional legacy multi-page variant metadata",
    )
    parser.add_argument(
        "--pdf-name",
        default="output_resume.pdf",
        help="Final PDF filename expected from Stage 3",
    )
    parser.add_argument(
        "--content-volume",
        choices=["light", "medium", "heavy", "not_required"],
        default=None,
        help="Optional Stage 2 single-page content volume label",
    )
    parser.add_argument(
        "--manifest-out",
        default=None,
        help="Optional explicit path for the handoff manifest",
    )
    args = parser.parse_args()
    normalized_layout_mode, normalized_multi_page_variant = normalize_layout_mode(
        args.layout_mode,
        args.multi_page_variant,
    )

    output_dir = Path(args.output_dir).resolve()
    raw_path = output_dir / "raw_content.md"
    refined_path = output_dir / "refined_resume.md"
    manifest_path = Path(args.manifest_out).resolve() if args.manifest_out else output_dir / "resume_pipeline_handoff.json"

    checks = []
    failures = []
    warnings = []

    raw_exists = raw_path.is_file()
    add_check(checks, "raw_content_exists", raw_exists, str(raw_path))
    if not raw_exists:
        failures.append("Missing raw_content.md")

    refined_exists = refined_path.is_file()
    add_check(checks, "refined_resume_exists", refined_exists, str(refined_path))
    if not refined_exists:
        failures.append("Missing refined_resume.md")

    if failures:
        result = {
            "valid": False,
            "manifest_written": False,
            "manifest_path": str(manifest_path),
            "checks": checks,
            "warnings": warnings,
            "failures": failures,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    raw_text = raw_path.read_text(encoding="utf-8", errors="replace")
    refined_text = refined_path.read_text(encoding="utf-8", errors="replace")

    raw_non_empty = bool(raw_text.strip())
    add_check(checks, "raw_content_non_empty", raw_non_empty, "raw_content.md should not be empty")
    if not raw_non_empty:
        failures.append("raw_content.md is empty")

    refined_non_empty = bool(refined_text.strip())
    add_check(checks, "refined_resume_non_empty", refined_non_empty, "refined_resume.md should not be empty")
    if not refined_non_empty:
        failures.append("refined_resume.md is empty")

    sections = parse_sections(refined_text)
    has_sections = bool(sections)
    add_check(checks, "section_headers_found", has_sections, f"found {len(sections)} section headers")
    if not has_sections:
        failures.append("No level-2 section headers found in refined_resume.md")

    forbidden_hits = [marker for marker in FORBIDDEN_MARKERS if marker in refined_text]
    add_check(
        checks,
        "forbidden_markers_absent",
        not forbidden_hits,
        "none found" if not forbidden_hits else ", ".join(forbidden_hits),
    )
    if forbidden_hits:
        failures.append("Forbidden process markers leaked into refined_resume.md")

    missing_type_annotations = []
    mismatched_type_annotations = []
    unknown_titles = []
    recognized_titles = []
    forbidden_section_titles = []

    for section in sections:
        title = section["title"]
        section_type = section["type"]
        expected = None
        if title in FORBIDDEN_SECTION_TITLES:
            forbidden_section_titles.append(title)
        if title in NARRATIVE_TITLES:
            expected = "narrative"
            recognized_titles.append(title)
        elif title in DATA_TITLES:
            expected = "data"
            recognized_titles.append(title)
        elif title in EDUCATION_TITLES:
            recognized_titles.append(title)
        else:
            unknown_titles.append(title)

        if expected and section_type is None:
            missing_type_annotations.append(title)
        elif expected and section_type != expected:
            mismatched_type_annotations.append(
                {"title": title, "expected": expected, "found": section_type}
            )

    add_check(
        checks,
        "recognized_ats_titles_present",
        bool(recognized_titles),
        ", ".join(recognized_titles) if recognized_titles else "none",
    )
    if not recognized_titles:
        failures.append("No recognized ATS-compatible section titles found")

    add_check(
        checks,
        "summary_sections_absent",
        not forbidden_section_titles,
        "none found" if not forbidden_section_titles else ", ".join(sorted(set(forbidden_section_titles))),
    )
    if forbidden_section_titles:
        failures.append("Summary/self-evaluation sections are not allowed in refined_resume.md")

    add_check(
        checks,
        "required_type_annotations_present",
        not missing_type_annotations and not mismatched_type_annotations,
        json.dumps(
            {
                "missing": missing_type_annotations,
                "mismatched": mismatched_type_annotations,
            },
            ensure_ascii=False,
        ),
    )
    if missing_type_annotations or mismatched_type_annotations:
        failures.append("Section type annotations are missing or incorrect")

    if unknown_titles:
        warnings.append(
            "Unknown section titles detected: " + ", ".join(sorted(set(unknown_titles)))
        )

    valid = not failures

    manifest = {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "layout_mode": normalized_layout_mode,
        "multi_page_variant": normalized_multi_page_variant,
        "input_layout_mode": args.layout_mode,
        "input_multi_page_variant": args.multi_page_variant,
        "pdf_name": args.pdf_name,
        "must_keep_files": ["raw_content.md", "refined_resume.md"],
        "stage1": {
            "artifact": "raw_content.md",
            "sha256": sha256_file(raw_path),
        },
        "stage2": {
            "artifact": "refined_resume.md",
            "sha256": sha256_file(refined_path),
            "validation_passed": valid,
            "content_volume": args.content_volume,
            "section_titles": [section["title"] for section in sections],
            "typed_sections": [section for section in sections if section["type"] is not None],
            "missing_type_annotations": missing_type_annotations,
            "unknown_titles": unknown_titles,
            "forbidden_section_titles": forbidden_section_titles,
            "forbidden_markers_found": forbidden_hits,
        },
        "stage3": {
            "artifact_html": "index.html",
            "artifact_pdf": args.pdf_name,
            "multi_page_variant": normalized_multi_page_variant,
            "text_rewrite_forbidden": True,
            "expected_refined_resume_sha256": sha256_file(refined_path),
        },
    }

    if (
        args.layout_mode != normalized_layout_mode
        or args.multi_page_variant != normalized_multi_page_variant
    ):
        warnings.append(
            "Legacy layout naming was normalized to "
            f"{normalized_layout_mode} / {normalized_multi_page_variant}"
    )
    if args.layout_mode == "Multi-Page Comfortable" and args.multi_page_variant == "not_required":
        warnings.append("Legacy Multi-Page Comfortable input is missing an explicit photo choice")
    if normalized_layout_mode in SINGLE_PAGE_LAYOUTS and args.multi_page_variant != "not_required":
        warnings.append("Single-page runs should not carry a multi-page variant")

    manifest_written = False
    if valid:
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        manifest_written = True

    result = {
        "valid": valid,
        "manifest_written": manifest_written,
        "manifest_path": str(manifest_path),
        "checks": checks,
        "warnings": warnings,
        "failures": failures,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if valid else 1


if __name__ == "__main__":
    sys.exit(main())
