# AI Resume Generator Skill | AI 简历自动生成Skill

<p align="center">
  <b>🌏 Language / 语言</b><br>
  <a href="./README.md">English</a> | <a href="./README_CN.md">简体中文</a>
</p>

> An AI-Native, beautifully crafted A4 Resume framework. Turns your messy notes into stunning PDF resumes.

## 🎯 Core Features
- **AI-Powered Transformation**: Includes a specially crafted Super System Prompt that guides LLMs to extract key information and output cross-page HTML strictly conforming to the CSS styles.
- **Smart Page Break**: Perfectly solves the common HTML-to-PDF issues of list truncation and excessive whitespace, ensuring every page has pixel-perfect margins.
- **One-Click Rendering**: Paired with a Playwright headless pipeline, enabling zero-config A4 PDF export from the terminal.

## 📦 Directory Structure
- `prompt_workflow.md`: The Super Prompt (AI Skill) to feed to your LLM (e.g., Cursor / Claude / ChatGPT). Just throw in your personal experience, and it will output perfect underlying HTML.
- `template_1page.css`: An ultra-compact single-page A4 template, designed for scenarios where a one-page resume is required (e.g., investment banks, multinational companies). Maximizes space utilization.
- `template_multipage.css`: A comfortable multi-page template with generous 20mm margins and physical page-break protection. Handles any length with natural cross-page layout.
- `builder.py`: The main Python script for rendering and exporting PDFs.
- `requirements.txt`: Python dependencies.

## 🚀 Quick Start

> **Requirement**: This project relies on Python for headless browser rendering. Please ensure `Python 3.8+` is installed on your machine.

### Method A: AI Agent Fully Automated Flow (Highly Recommended ✨)
If you are using an AI coding assistant such as `Antigravity`, `Cursor`, `Codex`, or `Claude Code`, you **don't need to** manually configure or run anything! Simply tell the AI the following "spell" in this directory:

> *"Please read my old resume, invoke the `SKILL.md` here, use the [Multi-Page] (or [Single-Page]) template to regenerate a beautiful resume named `my_new_resume.pdf`, and automatically execute all environment setup commands."*

The AI assistant will automatically read the `SKILL.md` in this repo, and handle the entire workflow for you — understanding your content, fetching CSS, writing HTML, configuring Python dependencies, and running the script — delivering a ready-made PDF straight to your hands!

### Method B: Manual Execution
*For situations without an AI coding assistant, relying only on a standard ChatGPT web interface to generate HTML.*

**Step 1: Prepare Content**
Open any web-based AI (e.g., ChatGPT), send it the contents of `prompt_workflow.md` from this directory, and request either the [Single-Page Compact] or [Multi-Page Comfortable] version to get an auto-generated `resume.html` file.

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### Step 3: Generate PDF
Place the AI-generated `resume.html` in this directory and run:
```bash
python builder.py resume.html
```
You will get a `resume.pdf` right in this directory, featuring flawless multi-page, auto line-break, anti-truncation Blue-Purple layout!

---

## ✨ What's New in v1.1.0

- **Adaptive Single-Page Layout Engine**: Added Step 2.5 with browser-based overflow detection and a 5-level progressive degradation strategy (L1–L5) that automatically adjusts line merging → column layouts → padding → font sizes → user prompt.
- **Dynamic Font-Size Injection**: Single-page CSS templates no longer preset `font-size`. The AI determines optimal sizes per content volume, maintaining a clear hierarchy (`h1 >> h2 > item-title ≥ body`, floor: 10pt).
- **Section-Level Column Layout**: New `.section-2col` / `.section-3col` CSS classes for column layout of entire sections — column count equals the number of sub-headings.
- **Line-Height Floor Lock**: Line-height is locked at ≥ 1.5 and excluded from any degradation strategy.
- **Windows Encoding Fix**: Added `PYTHONIOENCODING=utf-8` to prevent GBK encoding errors on Windows.
- **Non-Blocking Server**: HTTP server for overflow verification runs as fire-and-forget to avoid long blocking timeouts.

---

## 📄 License
GLP-3.0
