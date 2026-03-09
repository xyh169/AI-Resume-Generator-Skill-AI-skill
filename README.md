# Resume Pipeline — Fully Automated Resume Generation Workflow

<p align="center">
  <b>🌏 Language / 语言</b><br>
  English | <a href="README_CN.md">简体中文</a>
</p>

> An Agentic AI-driven, one-click end-to-end resume generation orchestration. Whether you input Word, PDF, HTML, plain text, or even highly colloquial **chat history and voice transcripts**, this workflow can transform the raw materials into a highly professional, beautifully typeset Blue-Purple style A4 PDF resume.

## 🎯 Core Architecture & Features Overview

This workflow acts as a Master Workflow scheduler, connecting the following three deeply enhanced, independent skills in a fixed sequence to provide an **end-to-end** solution from format parsing to typesetting rendering.

| Stage | Core Module | Advanced Features & Mechanisms |
|------|---------|--------------------|
| **1** | `1-template-to-md` | **Universal Format Support**: Fully supports parsing `PDF`, `DOCX`, `TXT`, `HTML`, `RTF`, `TEX`, and can even directly ingest **colloquial plain text / chat records / voice transcripts**.<br>Equipped with **5 Error Retries** and a **Multi-Strategy Fallback System** (e.g., PDF conversion prioritizes `pymupdf4llm`, falls back to native `PyMuPDF` on failure, and uses `pdfplumber` as a last resort; HTML and DOCX also have corresponding automatic fallback routing). Supports automatic installation of missing packages and binary tools. |
| **2** | `2-transcriptor` | **Automated Denoising & Professional Restructuring Engine**. Based on the user-provided target role/company, it automatically retrieves the latest Job Description (JD) from the web for deep matching. Leverages the **STAR method** to eliminate fluff, utilizes standardized professional action verbs (e.g., "Spearheaded", "Directed"), and strictly manages information boundaries (e.g., isolating honors and awards into separate sections). |
| **3** | `3-pdf-generator` | **Single/Multi-Page PDF Dynamic Typesetting Engine**. Built-in browser-based height detection monitors the A4 page's overflow/whitespace status. For the Single-Page Extreme version, it provides a **Dynamic Adaptive Layout Algorithm** (adjusting font size, margins, and column layouts) to hit the exact `90%-95%` optimal page space utilization rate, while **strictly upholding** the visual red line of a minimum line-height of `1.5`. |

## 📦 Directory Structure

```text
├── README.md                ← This English Document
├── README_CN.md             ← Chinese Document Version
└── resume-pipeline/         ← Core Pipeline Directory
    ├── SKILL.md                 ← Master Orchestration Entry Point
    ├── 1-template-to-md/        ← Stage 1: High-Tolerance Format Parsing & Conversion
    ├── 2-transcriptor/          ← Stage 2: JD-Matched Content Denoising & Restructuring
    └── 3-pdf-generator/         ← Stage 3: Adaptive A4 Layout Rendering & PDF Export
```

## ✨ What's New in v2.0.0 (Major Update)

Compared to the previous v1.x versions (which primarily focused on PDF generation and single-page adaptive layouts), v2.0.0 introduces a massive architectural upgrade:

*   **From Single Script to 3-Skill Synergy Orchestration**: Upgraded from a standalone PDF generator to a complete pipeline featuring **Format Parsing (template-to-md) → Content Transcription & Denoising (transcriptor) → Dynamic Rendering (pdf-generator)**.
*   **Universal Format Parsing**: Expanded input capabilities beyond just text. Now natively supports parsing and extracting data from `PDF`, `DOCX`, `TXT`, `HTML`, `RTF`, `TEX`, as well as parsing unstructured chat history and voice transcripts.
*   **Native MCP Protocol Support**: The newly added parsing and transcribing modules now support the Standardized Model Context Protocol (MCP). They can be directly mounted as independent server tools in AI IDEs like Cursor and Claude Desktop.

---

### Previous Updates (v1.1.0)
*   **Adaptive Single-Page Layout Engine**: Added Step 2.5 with browser-based overflow detection and a progressive degradation/expansion strategy.
*   **Dynamic Font-Size Injection**: The AI determines optimal font sizes based on content volume, maintaining clear visual hierarchy.
*   **Section-Level Column Layout**: Introduced CSS classes like `.section-2col` / `.section-3col` for automatic column alignment.
*   **Line-Height Safe Limit**: Built-in lock prevents line-heights below 1.5 during dynamic compression.


## 🚀 Recommended Integration & Usage

### Option A: AI Agent Fully Automated Mode (Recommended ✨)

In any IDE or application equipped with Agent capabilities (e.g., Cursor, Claude Desktop, Antigravity), issue the following prompt:

> *"Please read `resume-pipeline/SKILL.md` and use the raw materials (attachments, text) I provided to automatically generate a resume. The target position is [Company Name + Role / Specific JD Text]. Please render it as a single-page/multi-page PDF."*

The AI will automatically prospect the JD, restructure colloquial descriptions, and transparently fix the layout by running testing server measurements on-the-fly when encountering page overflow or excessive whitespace.

### Option B: Integration as Standardized MCP Servers 🔌

Our underlying capabilities support the Model Context Protocol (MCP). You can directly mount them as independent services (with built-in error retry and fallback systems) in your toolchain.
Ensure you have the `uv` package manager installed. Using Cursor as an example:
- **Format Parsing (`convert_file_to_md`)**: `uvx --from "/Your_Absolute_Path/1-template-to-md/mcp-server" mcp-template-to-md`
- **Content Restructuring (`transcriptor-agent`)**: `uvx --from "/Your_Absolute_Path/2-transcriptor/mcp-server" mcp-transcriptor`

*(For more advanced parameters, execution protocols, and system prompt configurations, please closely read the `SKILL.md` files within their respective sub-directories.)*

---

## 📄 License
GPL-3.0
