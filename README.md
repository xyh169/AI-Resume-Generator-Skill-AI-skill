# Resume Pipeline



<p align="left"><strong>Language:</strong> <a href="README.md">English</a> | <a href="README_CN.md">简体中文</a></p>

---

## Overview

Resume Pipeline turns messy resume materials into polished A4 resumes through a stable three-stage workflow.

It is designed for:

- job seekers who want higher-quality resumes than one-off prompting usually produces
- career coaches and resume writers who need repeatable delivery
- teams building resume-generation workflows around structured handoff and validation

Supported source materials include:

- `PDF`, `DOCX`, `TXT`, `HTML`, `RTF`, `TEX`
- pasted notes and rough drafts
- chat logs and interview notes
- transcript-style raw text

<a id="what-it-does"></a>

## What It Does

- Converts raw files and unstructured text into normalized Markdown source material.
- Rewrites content into ATS-friendly resume sections for a target role, company, or JD.
- Produces four fixed A4 layout modes instead of loosely styled output.
- Supports both single-page and multi-page delivery, with and without photo variants.

## Layout Modes

The workflow uses four explicit output modes:

- `Single-Page No Photo`
- `Single-Page With Photo`
- `Multi-Page With Photo`
- `Multi-Page No Photo`

## Workflow Structure

### Stage 1: `1-template-to-md`

- Reads raw input files or text material.
- Extracts text and structure.
- Writes normalized source material to `raw_content.md`.

### Stage 2: `2-transcriptor`

- Rewrites source material into a professional resume.
- Aligns content to a target role or JD.
- Enforces ATS-compatible section naming.
- Removes standalone summary / self-evaluation sections.
- Writes the final resume source to `refined_resume.md`.

### Stage 3: `3-pdf-generator`

- Maps Markdown into a fixed HTML structure.
- Applies the correct CSS branch for the selected layout.
- Measures and converges single-page layouts in the browser when required.
- Exports the final A4 PDF.

## Repository Structure

```text
.
├── README.md
├── README_CN.md
├── LICENSE
├── assets/
│   └── readme/
│       ├── case-single-page-no-photo.png
│       ├── case-single-page-photo.png
│       ├── case-multipage-no-photo.png
│       └── case-multipage-photo.png
└── resume-pipeline/
    ├── SKILL.md
    ├── 1-template-to-md/
    ├── 2-transcriptor/
    ├── 3-pdf-generator/
    └── validators/
```

<a id="case-gallery"></a>

## Case Gallery

<table>
  <tr>
    <td align="center" width="50%">
      <img src="assets/readme/case-single-page-no-photo.png" alt="Single-page no-photo resume sample" width="100%">
      <br>
      <sub><b>Single-Page No Photo</b></sub>
    </td>
    <td align="center" width="50%">
      <img src="assets/readme/case-single-page-photo.png" alt="Single-page with-photo resume sample" width="100%">
      <br>
      <sub><b>Single-Page With Photo</b></sub>
    </td>
  </tr>
  <tr>
    <td align="center" width="50%">
      <img src="assets/readme/case-multipage-no-photo.png" alt="Multi-page no-photo resume sample pages 1 and 2" width="100%">
      <br>
      <sub><b>Multi-Page No Photo</b> (Pages 1-2 merged horizontally)</sub>
    </td>
    <td align="center" width="50%">
      <img src="assets/readme/case-multipage-photo.png" alt="Multi-page with-photo resume sample pages 1 and 2" width="100%">
      <br>
      <sub><b>Multi-Page With Photo</b> (Pages 1-2 merged horizontally)</sub>
    </td>
  </tr>
</table>

<a id="how-to-use"></a>

## How To Use

### Recommended: agent workflow

Use the pipeline by asking an agent-capable environment to read the top-level workflow contract:

```text
Read resume-pipeline/SKILL.md and build a resume from my source materials.
Target role: [company + role] or [JD text].
Layout mode: Single-Page No Photo / Single-Page With Photo / Multi-Page With Photo / Multi-Page No Photo.
```

Typical inputs:

- one or more raw resume files
- pasted text notes
- a target role or JD
- an optional preferred layout mode

Typical outputs:

- `raw_content.md`
- `refined_resume.md`
- `index.html`
- `output_resume.pdf` (the final resume deliverable)

### For local workflow development

- Stage contracts are defined in `resume-pipeline/SKILL.md` and each stage subdirectory.
- Validation lives in `resume-pipeline/validators/`.
- Reusable local rendering helpers live in `resume-pipeline/3-pdf-generator/scripts/`.

## Validation

The repository includes validator scripts for the Stage 2 to Stage 3 handoff:

- `resume-pipeline/validators/validate_stage2.py`
- `resume-pipeline/validators/validate_stage3.py`

These checks help ensure:

- required artifacts exist
- Stage 2 output is structurally clean before rendering
- single-page outputs really remain single-page after PDF export

<a id="latest-updates"></a>

## v2.4.0 Updates

### Content rewriting updates

Updated in:

- `resume-pipeline/2-transcriptor/SKILL.md`
- `resume-pipeline/validators/validate_stage2.py`

What changed:

- standalone `Summary`, `个人总结`, and self-evaluation sections are blocked from final resumes
- single-page text density limits were relaxed so fuller resumes can still reach Stage 3
- single-page with photo now has safer Stage 2 expansion boundaries

### System updates

Updated in:

- `resume-pipeline/3-pdf-generator/SKILL.md`
- `resume-pipeline/3-pdf-generator/references/`
- `resume-pipeline/3-pdf-generator/resources/`

What changed:

- the layout contract now uses four explicit modes
- `Single-Page With Photo` is treated as a dedicated branch, not a cosmetic variant
- multi-page with-photo and no-photo branches were clarified and separated

### Rendering and validation helpers

Updated in:

- `resume-pipeline/3-pdf-generator/scripts/`
- `resume-pipeline/validators/validate_stage3.py`

What changed:

- reusable local rendering helpers were added for single-page photo and multi-page branches
- Stage 3 validation was tightened around layout consistency and final artifact checks

<a id="license"></a>

## License

GPL-3.0
