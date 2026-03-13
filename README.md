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
| **3** | `3-pdf-generator` | **Single/Multi-Page PDF Dynamic Typesetting Engine**. Supports `Single-Page Extreme` plus `Multi-Page Comfortable` with two variants: `With Photo` and `No Photo`. Single-page mode includes browser-based height detection and a **Dynamic Adaptive Layout Algorithm** (adjusting font size, margins, and column layouts) to hit the `93%-98%` page utilization target while **ensuring** a minimum line-height of `1.5`; multi-page mode uses shared cross-page rules without the single-page convergence loop. |

## 📦 Directory Structure

```text
├── README.md                ← This English Document
├── README_CN.md             ← Chinese Document Version
└── resume-pipeline/         ← Core Pipeline Directory
    ├── SKILL.md                 ← Master Orchestration Entry Point
    ├── REFACTOR_PLAN.md         ← Refactor Roadmap / Progress Tracker
    ├── 1-template-to-md/        ← Stage 1: High-Tolerance Format Parsing & Conversion
    ├── 2-transcriptor/          ← Stage 2: JD-Matched Content Denoising & Restructuring
    ├── 3-pdf-generator/         ← Stage 3: Adaptive A4 Layout Rendering & PDF Export
    │   └── references/          ← Single-page / multi-page shared + variant references
    └── validators/              ← Minimal stage validators & handoff checks
```

## ✨ What's New in v2.2.0

This release combines **multi-page layout refinement** with **workflow execution hardening**. 

*   **Pipeline Contract Hardening Across All Skills**: Refactored the master workflow and all three stage skills into a lower-freedom execution protocol with explicit `HARD CONTRACT`, stage ownership, pass conditions, artifact requirements, and failure handling. This reduces cross-stage drift and makes the pipeline easier for weaker models to follow consistently.
*   **Minimal Validators + Handoff Manifest Layer**: Added lightweight Stage 2 / Stage 3 validators plus a generated `resume_pipeline_handoff.json` manifest. The pipeline can now verify key artifacts, catch leaked process markers, ensure Stage 3 does not silently rewrite `refined_resume.md`, and confirm single-page PDF outputs are truly one page.
*   **Stage 3 Reference Split for Single-Page vs Multi-Page Variants**: Reorganized the PDF generator so the main `SKILL.md` acts as the routing contract, while `references/single-page-mode.md`, `references/multi-page-mode.md`, and the multi-page variant references hold the branch-specific rules. This keeps the top-level instructions shorter and makes branch selection clearer.
*   **Multi-Page Dual Variants (With Photo / No Photo)**: Expanded multi-page mode into two explicit variants. `With Photo` keeps the original `Basic Information + right-side photo/photo-slot` layout, while `No Photo` uses a cleaner header-first structure without reserving image space. Both variants share the same cross-page behavior and content-aware blue guide line rules, making it easier to support both domestic photo-style resumes and cleaner no-photo formats without overhauling the rest of the template.
*   **Content-Aware Blue Guide Line Rendering**: Upgraded the multi-page left-side blue guide line logic so it now follows **real content blocks** instead of stretching across empty tail space. The guide line remains visually continuous when more content exists below, but no longer drops awkwardly into blank page-bottom areas.
*   **Single-Page Content Gate Recalibration**: Relaxed the `2-transcriptor` single-page precheck thresholds for bullet count, effective character count, and estimated render lines, so dense-but-still-readable resumes can pass without being over-compressed at the content stage. 

---

## 🗂 Historical Updates Archive

### v2.1.0

This release focuses on typesetting engine logic refinement and ATS (Applicant Tracking System) compatibility enhancements:

*   **ATS-Compatible Standardized Section Titles**: Introduced a comprehensive Chinese/English ATS standard title mapping table and selection rules in `2-transcriptor`. Ensures all output section titles (e.g., "Education", "Projects", "Skills") are 100% parseable by mainstream applicant tracking systems and AI resume scoring engines, eliminating information loss or score penalties caused by non-standard headings.
*   **Optimized Layout Logic & Ordering**: Refactored the degradation/expansion strategy execution order and closed-loop verification flow in `3-pdf-generator`. Introduced a "Degrade-then-Backfill" closed-loop mechanism (L1→L2→L3→L4 progressive degradation, with automatic E1–E4 expansion triggered if usage drops too low), ensuring page utilization converges to the 93%–98% sweet spot before PDF export — preventing both over-compression and excessive whitespace.
*   **User Parameter Guidance & Transparent Choices**: Improved the workflow entry's user interaction — the top-level layout choice remains only "Single-Page Extreme" or "Multi-Page Comfortable", and multi-page runs now include a second-step variant choice (`With Photo` / `No Photo`). The system still handles content feasibility automatically, and the loop termination messaging now provides clearer actionable suggestions.
*   **Section Content Type Annotation System**: Added `<!-- type: narrative -->` and `<!-- type: data -->` annotation conventions, enabling the Transcriptor's output to be precisely recognized by the downstream PDF engine for intelligent column layout decisions — narrative sections never use columns, data sections adopt columns on demand.

---

### v2.0.0

Compared to the previous v1.x versions (which primarily focused on PDF generation and single-page adaptive layouts), v2.0.0 introduces a major architectural upgrade:

*   **From Single Script to 3-Skill Synergy Orchestration**: Upgraded from a standalone PDF generator to a complete pipeline featuring **Format Parsing (template-to-md) → Content Transcription & Denoising (transcriptor) → Dynamic Rendering (pdf-generator)**.
*   **Universal Format Parsing**: Expanded input capabilities beyond just text. Now natively supports parsing and extracting data from `PDF`, `DOCX`, `TXT`, `HTML`, `RTF`, `TEX`, as well as parsing unstructured chat history and voice transcripts.
*   **Native MCP Protocol Support**: The newly added parsing and transcribing modules now support the Standardized Model Context Protocol (MCP). They can be directly mounted as independent server tools in AI IDEs like Cursor and Claude Desktop.

---

### v1.1.0
*   **Adaptive Single-Page Layout Engine**: Added Step 2.5 with browser-based overflow detection and a progressive degradation/expansion strategy.
*   **Dynamic Font-Size Injection**: The AI determines optimal font sizes based on content volume, maintaining clear visual hierarchy.
*   **Section-Level Column Layout**: Introduced CSS classes like `.section-2col` / `.section-3col` for automatic column alignment.
*   **Line-Height Safe Limit**: Built-in lock prevents line-heights below 1.5 during dynamic compression.

## 🧭 Layout Selection Flow

1. Choose `Single-Page Extreme` or `Multi-Page Comfortable`.
2. If you choose `Multi-Page Comfortable`, then choose `With Photo` or `No Photo`.
3. If you do not provide a JD / company + role / target direction, the workflow will ask once before falling back to a generic version.

## 🚀 Recommended Integration & Usage

### Option A: AI Agent Fully Automated Mode (Recommended ✨)

In any IDE or application equipped with Agent capabilities (e.g., Cursor, Claude Desktop, Antigravity), issue the following prompt:

> *"Please read `resume-pipeline/SKILL.md` and use the raw materials (attachments, text) I provided to automatically generate a resume. The target position is [Company + Role / Specific JD Text]. Please render it as `Single-Page Extreme` or `Multi-Page Comfortable`. If using multi-page, choose `With Photo` or `No Photo`."*

If you provide a target company/role, the AI will automatically retrieve the latest JD, restructure colloquial descriptions, and transparently fix layout issues when needed. If you do **not** provide a target direction, the workflow will first ask whether you want to specify one or proceed with a generic version.

### Option B: Integration as Standardized MCP Servers 🔌

Our underlying capabilities support the Model Context Protocol (MCP). You can directly mount them as independent services (with built-in error retry and fallback systems) in your toolchain.
Ensure you have the `uv` package manager installed. Using Cursor as an example:
- **Format Parsing (`convert_file_to_md`)**: `uvx --from "/Your_Absolute_Path/1-template-to-md/mcp-server" mcp-template-to-md`
- **Content Restructuring (`transcriptor-agent`)**: `uvx --from "/Your_Absolute_Path/2-transcriptor/mcp-server" mcp-transcriptor`

*(For more advanced parameters, execution protocols, and system prompt configurations, please closely read the `SKILL.md` files within their respective sub-directories.)*

---

## 📄 License
GPL-3.0
