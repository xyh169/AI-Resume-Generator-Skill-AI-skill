from __future__ import annotations

import argparse
import html
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[3]
CSS_PATH = ROOT / "resume-pipeline" / "3-pdf-generator" / "resources" / "template_multipage-2.css"


@dataclass
class Section:
    title: str
    section_type: str
    lines: list[str]


def trim_blank_edges(lines: Iterable[str]) -> list[str]:
    buf = list(lines)
    while buf and not buf[0].strip():
        buf.pop(0)
    while buf and not buf[-1].strip():
        buf.pop()
    return buf


def parse_resume(md_text: str) -> tuple[str, str, list[Section]]:
    lines = md_text.splitlines()
    name = ""
    contact = ""
    sections: list[Section] = []
    current_title = None
    current_type = "narrative"
    current_lines: list[str] = []

    for raw in lines:
        line = raw.rstrip().lstrip("\ufeff")
        if line.startswith("# "):
            name = line[2:].strip()
            continue
        heading = re.match(r"^##\s+(.+?)(?:\s*<!--\s*type:\s*(\w+)\s*-->)?\s*$", line)
        if heading:
            if current_title:
                sections.append(Section(current_title, current_type, trim_blank_edges(current_lines)))
            current_title = heading.group(1).strip()
            current_type = (heading.group(2) or "narrative").strip()
            current_lines = []
            continue
        if not current_title and line.strip():
            if not contact:
                contact = line.strip()
            continue
        if current_title is not None:
            current_lines.append(line)

    if current_title:
        sections.append(Section(current_title, current_type, trim_blank_edges(current_lines)))
    return name, contact, sections


def escape(text: str) -> str:
    return html.escape(text, quote=True)


def render_inline(text: str) -> str:
    pieces = re.split(r"(\*\*.+?\*\*)", text)
    rendered: list[str] = []
    for piece in pieces:
        if piece.startswith("**") and piece.endswith("**") and len(piece) >= 4:
            rendered.append(f'<span class="k">{escape(piece[2:-2].strip())}</span>')
        else:
            rendered.append(escape(piece))
    return "".join(rendered)


def split_pipes(text: str) -> list[str]:
    return [segment.strip() for segment in text.split("|")]


def strip_md_bold(text: str) -> str:
    return re.sub(r"^\*\*(.+?)\*\*$", r"\1", text).strip()


def parse_basic_info(line: str) -> list[tuple[str, str]]:
    items: list[tuple[str, str]] = []
    for part in [piece.strip() for piece in line.split("|") if piece.strip()]:
        match = re.match(r"^\*\*(.+?)\*\*\s*:\s*(.+)$", part)
        if match:
            items.append((match.group(1).strip(), match.group(2).strip()))
        elif ":" in part:
            key, value = part.split(":", 1)
            items.append((key.strip(), value.strip()))
        else:
            items.append(("", part))
    return items


def render_contact_line(items: list[tuple[str, str]]) -> str:
    rendered = []
    for label, value in items:
        if label:
            rendered.append(f"<strong>{escape(label)}</strong>: {escape(value)}")
        else:
            rendered.append(escape(value))
    return " | ".join(rendered)


def render_education(section: Section) -> str:
    items: list[str] = []
    for raw in section.lines:
        line = raw.strip()
        if not line.startswith("- "):
            continue
        body = line[2:].strip()
        school, major, degree, date = (split_pipes(body) + ["", "", "", ""])[:4]
        items.append(
            "".join(
                [
                    '<div class="item edu-item">',
                    '<div class="edu-header">',
                    "<div>",
                    f'<span class="edu-school">{escape(strip_md_bold(school))}</span>',
                    f'<span class="edu-major"> | {escape(major)}</span>' if major else "",
                    f'<span class="edu-detail"> | {escape(degree)}</span>' if degree else "",
                    "</div>",
                    f'<div class="item-date">{escape(date)}</div>' if date else "",
                    "</div>",
                    "</div>",
                ]
            )
        )
    return (
        '<div class="section">'
        f'<div class="section-title"><h2>{escape(section.title)}</h2></div>'
        f'<div class="section-content">{"".join(items)}</div>'
        "</div>"
    )


def parse_narrative_items(section: Section) -> list[dict[str, object]]:
    items: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    for raw in section.lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("- "):
            if current is None:
                current = {"header": "", "bullets": []}
            bullets = current["bullets"]
            if isinstance(bullets, list):
                bullets.append(line[2:].strip())
            continue
        if current is not None:
            items.append(current)
        current = {"header": line, "bullets": []}
    if current is not None:
        items.append(current)
    return items


def render_narrative(section: Section) -> str:
    items_html: list[str] = []
    for item in parse_narrative_items(section):
        header = str(item["header"])
        title = ""
        org = ""
        date = ""
        parts = split_pipes(header)
        if len(parts) >= 3:
            title, org, date = parts[0], parts[1], " | ".join(parts[2:])
        elif len(parts) == 2:
            title, org = parts[0], parts[1]
        elif len(parts) == 1:
            title = parts[0]
        title = strip_md_bold(title)
        org = strip_md_bold(org)
        bullets = item["bullets"] if isinstance(item["bullets"], list) else []
        bullet_html = "".join(f"<li>{render_inline(str(bullet))}</li>" for bullet in bullets)
        items_html.append(
            "".join(
                [
                    '<div class="item">',
                    '<div class="item-header">',
                    "<div>",
                    f'<span class="item-title">{escape(title)}</span>' if title else "",
                    f'<span class="item-org">| {escape(org)}</span>' if org else "",
                    "</div>",
                    f'<div class="item-date">{escape(date)}</div>' if date else "",
                    "</div>",
                    f"<ul>{bullet_html}</ul>" if bullet_html else "",
                    "</div>",
                ]
            )
        )
    return (
        '<div class="section">'
        f'<div class="section-title"><h2>{escape(section.title)}</h2></div>'
        f'<div class="section-content">{"".join(items_html)}</div>'
        "</div>"
    )


def render_data(section: Section) -> str:
    bullets: list[str] = []
    for raw in section.lines:
        line = raw.strip()
        if line.startswith("- "):
            bullets.append(f"<li>{render_inline(line[2:].strip())}</li>")
    return (
        '<div class="section">'
        f'<div class="section-title"><h2>{escape(section.title)}</h2></div>'
        f'<div class="section-content"><div class="item"><ul>{"".join(bullets)}</ul></div></div>'
        "</div>"
    )


def add_optional_section_class(section_html: str, section_title: str, page_break_titles: set[str]) -> str:
    if section_title in page_break_titles:
        return section_html.replace('<div class="section">', '<div class="section page-break-before">', 1)
    return section_html


def build_html(name: str, contact: str, sections: list[Section], page_break_titles: set[str]) -> str:
    css_text = CSS_PATH.read_text(encoding="utf-8")
    basic_info = parse_basic_info(contact)
    edu_section = sections[0] if sections else None
    body_sections = sections[1:] if len(sections) > 1 else []

    rendered_sections: list[str] = []
    if edu_section:
        rendered_sections.append(
            add_optional_section_class(
                render_education(edu_section),
                edu_section.title,
                page_break_titles,
            )
        )

    for section in body_sections:
        if section.section_type == "data":
            section_html = render_data(section)
        else:
            section_html = render_narrative(section)
        rendered_sections.append(add_optional_section_class(section_html, section.title, page_break_titles))

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(name)} - Resume</title>
<style>
{css_text}
body {{
    font-family: Arial, "Microsoft YaHei", "微软雅黑", SimSun, "宋体", sans-serif;
    font-size: 10pt;
    line-height: 1.35;
}}
.header {{
    text-align: center;
}}
.header h1 {{
    font-size: 22pt;
}}
.header p {{
    font-size: 10pt;
    line-height: 1.35;
}}
.section-title h2 {{
    font-size: 11.5pt;
}}
.item-title {{
    font-size: 10.2pt;
}}
.item-org,
.item-date,
.edu-school,
.edu-major,
.edu-detail,
li {{
    font-size: 10pt;
}}
</style>
</head>
<body>
<div class="a4-page">
  <div class="header">
    <h1>{escape(name)}</h1>
    <p>{render_contact_line(basic_info)}</p>
  </div>
  {"".join(rendered_sections)}
</div>
</body>
</html>
"""


def render_outputs(index_path: Path, preview_path: Path | None, pdf_path: Path) -> dict[str, str]:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 1600}, device_scale_factor=1)
        page.goto(index_path.resolve().as_uri(), wait_until="networkidle")
        if preview_path is not None:
            page.screenshot(path=str(preview_path), full_page=True)
        page.pdf(
            path=str(pdf_path),
            format="A4",
            prefer_css_page_size=True,
            print_background=True,
            scale=1,
        )
        browser.close()
    return {
        "html": str(index_path),
        "preview": str(preview_path) if preview_path else "",
        "pdf": str(pdf_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a multi-page no-photo resume from refined_resume.md.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--preview", type=Path, default=None)
    parser.add_argument("--result", type=Path, default=None)
    parser.add_argument(
        "--page-break-before-title",
        action="append",
        default=[],
        help="Section title that should start on a new page. Can be passed multiple times.",
    )
    args = parser.parse_args()

    md_text = args.input.read_text(encoding="utf-8")
    name, contact, sections = parse_resume(md_text)
    html_text = build_html(name, contact, sections, set(args.page_break_before_title))
    args.index.write_text(html_text, encoding="utf-8")
    result = render_outputs(args.index, args.preview, args.pdf)
    if args.result:
        args.result.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
