from __future__ import annotations

import argparse
import html
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[4]
CSS_PATH = ROOT / "resume-pipeline" / "resume-pipeline" / "3-pdf-generator" / "resources" / "template_1page_photo.css"


@dataclass
class Section:
    title: str
    section_type: str
    lines: list[str]

    @property
    def char_count(self) -> int:
        total = 0
        for line in self.lines:
            stripped = line.strip()
            if stripped.startswith("- "):
                stripped = stripped[2:].strip()
            total += len(re.sub(r"\*\*(.+?)\*\*", r"\1", stripped))
        return total


def parse_resume(md_text: str) -> tuple[str, str, list[Section]]:
    lines = md_text.splitlines()
    name = ""
    contact = ""
    sections: list[Section] = []
    current_title = None
    current_type = "narrative"
    current_lines: list[str] = []

    for raw in lines:
        line = raw.rstrip()
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


def trim_blank_edges(lines: Iterable[str]) -> list[str]:
    buf = list(lines)
    while buf and not buf[0].strip():
        buf.pop(0)
    while buf and not buf[-1].strip():
        buf.pop()
    return buf


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
                    '<div class="edu-item">',
                    '<div class="edu-header">',
                    "<div>",
                    f'<span class="edu-school">{escape(school)}</span>',
                    f'<span class="edu-major"> | {escape(major)}</span>' if major else "",
                    f'<span class="edu-detail"> | {escape(degree)}</span>' if degree else "",
                    "</div>",
                    f'<span class="item-date">{escape(date)}</span>' if date else "",
                    "</div>",
                    "</div>",
                ]
            )
        )
    return (
        '<section class="section">'
        f'<div class="section-title"><h2>{escape(section.title)}</h2></div>'
        f'<div class="section-content">{"".join(items)}</div>'
        "</section>"
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
            cast_list(current["bullets"]).append(line[2:].strip())
            continue
        if current is not None:
            items.append(current)
        current = {"header": line, "bullets": []}
    if current is not None:
        items.append(current)
    return items


def cast_list(value: object) -> list[str]:
    return value if isinstance(value, list) else []


def render_narrative(section: Section) -> str:
    items_html: list[str] = []
    for item in parse_narrative_items(section):
        header = str(item["header"])
        title = ""
        org = ""
        date = ""
        if header:
            parts = split_pipes(header)
            if len(parts) >= 3:
                title, org, date = parts[0], parts[1], " | ".join(parts[2:])
            elif len(parts) == 2:
                title, org = parts[0], parts[1]
            elif len(parts) == 1:
                title = parts[0]
        title = re.sub(r"^\*\*(.+?)\*\*$", r"\1", title).strip()
        org = re.sub(r"^\*\*(.+?)\*\*$", r"\1", org).strip()
        bullet_html = "".join(f"<li>{render_inline(bullet)}</li>" for bullet in cast_list(item["bullets"]))
        items_html.append(
            "".join(
                [
                    '<div class="item">',
                    '<div class="item-header">' if header else "",
                    "<div>" if header else "",
                    f'<span class="item-title">{escape(title)}</span>' if title else "",
                    f'<span class="item-org">| {escape(org)}</span>' if org else "",
                    "</div>" if header else "",
                    f'<span class="item-date">{escape(date)}</span>' if date else "",
                    "</div>" if header else "",
                    f"<ul>{bullet_html}</ul>" if bullet_html else "",
                    "</div>",
                ]
            )
        )
    return (
        '<section class="section">'
        f'<div class="section-title"><h2>{escape(section.title)}</h2></div>'
        f'<div class="section-content">{"".join(items_html)}</div>'
        "</section>"
    )


def render_data(section: Section, section_content_class: str = "") -> str:
    bullet_html = []
    for raw in section.lines:
        line = raw.strip()
        if line.startswith("- "):
            bullet_html.append(f"<li>{render_inline(line[2:].strip())}</li>")
    content_class = "section-content"
    if section_content_class:
        content_class += f" {section_content_class}"
    return (
        '<section class="section">'
        f'<div class="section-title"><h2>{escape(section.title)}</h2></div>'
        f'<div class="{content_class}"><ul>{"".join(bullet_html)}</ul></div>'
        "</section>"
    )


def group_data_sections(data_sections: list[Section]) -> tuple[list[Section], set[str], str]:
    if len(data_sections) < 2:
        return data_sections, set(), ""
    ordered = sorted(data_sections, key=lambda sec: sec.char_count, reverse=True)
    if len(ordered) >= 3:
        tail2 = ordered[-2:]
        tail3 = ordered[-3:]
        diff2 = max(sec.char_count for sec in tail2) - min(sec.char_count for sec in tail2)
        diff3 = max(sec.char_count for sec in tail3) - min(sec.char_count for sec in tail3)
        if diff2 <= diff3:
            group = tail2
            row_class = "data-sections-row"
        else:
            group = tail3
            row_class = "data-sections-row-3"
    else:
        group = ordered
        row_class = "data-sections-row"
    group_titles = {sec.title for sec in group}
    return ordered, group_titles, row_class


def render_body_sections(sections: list[Section], use_l2: bool) -> tuple[str, list[str]]:
    narrative = [sec for sec in sections if sec.section_type != "data"]
    data_sections = [sec for sec in sections if sec.section_type == "data"]
    section_html: list[str] = []
    rendered_titles: list[str] = []

    for sec in narrative:
        section_html.append(render_narrative(sec))
        rendered_titles.append(sec.title)

    ordered_data = data_sections
    grouped_titles: set[str] = set()
    row_class = ""
    if use_l2:
        ordered_data, grouped_titles, row_class = group_data_sections(data_sections)

    if ordered_data and grouped_titles and row_class:
        regular = [sec for sec in ordered_data if sec.title not in grouped_titles]
        grouped = [sec for sec in ordered_data if sec.title in grouped_titles]
        for sec in regular:
            section_html.append(render_data(sec))
            rendered_titles.append(sec.title)
        section_html.append(
            f'<div class="{row_class}">'
            + "".join(render_data(sec) for sec in grouped)
            + "</div>"
        )
        rendered_titles.extend(sec.title for sec in grouped)
    else:
        for sec in ordered_data:
            content_class = ""
            if use_l2 and len(ordered_data) == 1:
                bullet_count = sum(1 for line in sec.lines if line.strip().startswith("- "))
                if bullet_count >= 4:
                    content_class = "section-2col"
            section_html.append(render_data(sec, content_class))
            rendered_titles.append(sec.title)

    return "".join(section_html), rendered_titles


def build_html(name: str, basic_info: list[tuple[str, str]], edu_section: Section | None, body_sections: list[Section], use_l2: bool) -> tuple[str, list[str]]:
    css_text = CSS_PATH.read_text(encoding="utf-8")
    intro_lines = []
    for label, value in basic_info:
        if label:
            intro_lines.append(
                '<div class="single-page-photo-basic-line">'
                f'<span class="single-page-photo-basic-label">{escape(label)}</span>'
                f'<span class="single-page-photo-basic-value">{escape(value)}</span>'
                "</div>"
            )
        else:
            intro_lines.append(
                '<div class="single-page-photo-basic-line">'
                f'<span class="single-page-photo-basic-value">{escape(value)}</span>'
                "</div>"
            )
    edu_html = render_education(edu_section) if edu_section else ""
    body_html, rendered_titles = render_body_sections(body_sections, use_l2)
    html_text = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{escape(name)} - Single Page Photo</title>
  <style>
{css_text}
    body {{
      font-family: Arial, "Microsoft YaHei", "微软雅黑", SimSun, "宋体", sans-serif;
      font-size: 9.5pt;
      line-height: 1.5;
    }}
    .a4-page {{
      padding: 10mm 13mm 10mm 13mm;
    }}
    .single-page-photo-hero {{
      column-gap: 10mm;
      margin-bottom: 4px;
    }}
    .header {{
      margin-bottom: 4px;
    }}
    .header h1 {{
      font-size: 17pt;
      line-height: 1.1;
    }}
    .single-page-photo-basic-info {{
      column-gap: 12px;
      row-gap: 3px;
    }}
    .single-page-photo-basic-line {{
      gap: 6px;
    }}
    .section {{
      margin-bottom: 2px;
    }}
    .section-title {{
      margin: 2px 0 1px 0;
      padding: 3px 16px 3px 8px;
    }}
    .section-title h2 {{
      font-size: 10pt;
    }}
    .section-content {{
      margin-bottom: 1px;
    }}
    .item {{
      margin-bottom: 1px;
    }}
    .item-header {{
      margin-bottom: 0;
      gap: 6px;
    }}
    .item-title, .item-org, .item-date, .edu-school, .edu-major, .single-page-photo-basic-label {{
      font-size: 1em;
    }}
    .single-page-photo-basic-value, .edu-detail, li, .header p {{
      font-size: 0.96em;
    }}
    ul {{
      margin: 0;
      padding-left: 1em;
    }}
    li {{
      margin-bottom: 1px;
    }}
    li::before {{
      left: -0.85em;
    }}
  </style>
</head>
<body>
  <div class="a4-page">
    <div class="single-page-photo-hero">
      <div class="single-page-photo-intro">
        <header class="header"><h1>{escape(name)}</h1></header>
        <div class="single-page-photo-basic-info">{"".join(intro_lines)}</div>
        {edu_html}
      </div>
      <div class="single-page-photo-aside">
        <div class="sidebar-photo"><div class="photo-slot">照片位</div></div>
      </div>
    </div>
    {body_html}
  </div>
</body>
</html>
"""
    return html_text, rendered_titles


def measure_page(page) -> dict[str, float | int]:
    return page.eval_on_selector(
        ".a4-page",
        """el => {
            const prev = {
                overflow: el.style.overflow,
                maxHeight: el.style.maxHeight,
                minHeight: el.style.minHeight,
                height: el.style.height
            };
            el.style.overflow = 'visible';
            el.style.maxHeight = 'none';
            el.style.minHeight = '0';
            el.style.height = 'auto';
            const contentHeight = Math.round(el.scrollHeight);
            const a4Height = 1123;
            const gap = a4Height - contentHeight;
            const usage = Number((contentHeight / a4Height * 100).toFixed(2));
            el.style.overflow = prev.overflow;
            el.style.maxHeight = prev.maxHeight;
            el.style.minHeight = prev.minHeight;
            el.style.height = prev.height;
            return { contentHeight, a4Height, gap, usage };
        }""",
    )


def render_and_measure(index_path: Path, preview_path: Path, pdf_path: Path) -> dict[str, float | int]:
    url = index_path.resolve().as_uri()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 1600}, device_scale_factor=1)
        page.goto(url, wait_until="networkidle")
        measure = measure_page(page)
        page.locator(".a4-page").screenshot(path=str(preview_path))
        page.pdf(
            path=str(pdf_path),
            format="A4",
            prefer_css_page_size=True,
            print_background=True,
            scale=1,
        )
        browser.close()
    return measure


def main() -> None:
    parser = argparse.ArgumentParser(description="Render the local single-page photo sample.")
    parser.add_argument("--input", type=Path, default=ROOT / "refined_resume3.md")
    parser.add_argument("--index", type=Path, default=ROOT / "index.html")
    parser.add_argument("--preview", type=Path, default=ROOT / "single_page_photo_preview.png")
    parser.add_argument("--pdf", type=Path, default=ROOT / "refined_resume3_single_page_photo.pdf")
    parser.add_argument("--measure", type=Path, default=ROOT / "single_page_photo_measure.json")
    args = parser.parse_args()

    md_text = args.input.read_text(encoding="utf-8")
    name, contact, sections = parse_resume(md_text)
    basic_info = parse_basic_info(contact)
    edu_section = sections[0] if sections else None
    body_sections = sections[1:] if len(sections) > 1 else []

    html_without_l2, order_without_l2 = build_html(name, basic_info, edu_section, body_sections, use_l2=False)
    args.index.write_text(html_without_l2, encoding="utf-8")
    measure = render_and_measure(args.index, args.preview, args.pdf)
    use_l2 = bool(measure["usage"] > 100 and any(sec.section_type == "data" for sec in body_sections))
    rendered_order = order_without_l2

    if use_l2:
        html_with_l2, rendered_order = build_html(name, basic_info, edu_section, body_sections, use_l2=True)
        args.index.write_text(html_with_l2, encoding="utf-8")
        measure = render_and_measure(args.index, args.preview, args.pdf)

    result = {
        "input": str(args.input),
        "html": str(args.index),
        "preview": str(args.preview),
        "pdf": str(args.pdf),
        "useL2": use_l2,
        "usage": measure["usage"],
        "contentHeight": measure["contentHeight"],
        "a4Height": measure["a4Height"],
        "gap": measure["gap"],
        "sectionOrder": rendered_order,
    }
    args.measure.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
