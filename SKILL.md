---
name: Generate Blue-Purple Flag Resume
description: An end-to-end automated workflow for Antigravity, Cursor, and other Agentic AIs to digest any user document and generate a perfectly formatted, page-break-proof A4 PDF resume in either single-page or multi-page layouts.
---

# Blue-Purple Resume Workflow Skill

You are an expert AI Assistant tasked with converting a user's raw, unstructured profile (from a Word document, TXT, or chat history) into a professionally designed, A4-ready PDF resume.

## Prerequisites & Environment
1. Ensure Python 3 is installed and available in the terminal.
2. Ensure the required packages are installed by running:
   `pip install -r requirements.txt`
3. Ensure Playwright browser binaries are present:
   `playwright install chromium`

## Workflow Steps

**Step 1: Understand User Requirements**
- Identify the source material (the user's unstructured text, DOCX, etc.).
- Identify the user's preferred layout: `Single-Page Extreme` (uses `template_1page.css`) or `Multi-Page Comfortable` (uses `template_multipage.css`). If not specified, ask the user or default to `Multi-Page Comfortable`.

**Step 2: Generate the HTML Structure**
You must act as the CSS/DOM architect and generate an `index.html` file in the current directory.
1. Read the exact content of the chosen CSS file (`template_1page.css` or `template_multipage.css`) from this repository.
2. Extract the user's professional information and map it strictly to the following DOM structure. DO NOT invent new classes.
3. **Dynamic Font-Size Injection**: The CSS template does NOT preset `font-size`. You must determine appropriate font sizes based on content volume and inject them into the `<style>` block.

### Font-Size Guidelines

- **No hard constraints**: Font sizes are entirely at your discretion based on content volume, aesthetics, and readability.
- **Clear hierarchy**: Each level should be visually smaller than the one above (even 0.5pt difference is sufficient).
- **Minimum floor**: The smallest font-size must not go below **10pt**.
- **Goal**: Beautiful, clearly layered, highly readable.

Recommended hierarchy (for reference, not mandatory):
```
h1 (name) >> h2 (section title) > item-title (entry title) ≥ body (body text)
```

### Line-Height Rule

> 🔒 **Line-height minimum is 1.5. This MUST NOT be reduced under any degradation strategy.**

### HTML Skeleton

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        /* INJECT THE ENTIRE CHOSEN CSS HERE */
        /* THEN INJECT font-size RULES */
    </style>
</head>
<body>
    <div class="a4-page">
        <!-- Header -->
        <div class="header">
            <h1>Candidate Name</h1>
            <p><strong>Phone</strong>: ... | <strong>Email</strong>: ...</p>
        </div>
        
        <!-- Section Example -->
        <div class="section">
            <div class="section-title"><h2>Experience</h2></div>
            <div class="section-content">
                <div class="item">
                    <div class="item-header">
                        <div><span class="item-title">Role</span><span class="item-org">| Company</span></div>
                        <div class="item-date">Date</div>
                    </div>
                    <ul>
                        <li><span class="k">Highlight</span>: Detail using STAR method...</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- Section-Level Column Layout Example -->
        <!-- Column count = number of sub-headings in the section -->
        <div class="section">
            <div class="section-title"><h2>Achievements & Honors</h2></div>
            <!-- 3 sub-items → section-3col -->
            <div class="section-content section-3col">
                <div class="item">...</div>
                <div class="item">...</div>
                <div class="item">...</div>
            </div>
        </div>
    </div>
</body>
</html>
```

**Step 2.5: Browser Overflow Verification & Adaptive Layout (Single-Page Mode Only)**

For `Single-Page Extreme` mode, you MUST verify that the content height fits within the A4 boundary after generating the HTML, and dynamically adjust layout parameters based on the result.

### 2.5.1 Verification Setup

1. Start a local HTTP server (run in background, fire-and-forget):
   `python -m http.server 8766`
   (Run in the directory containing `index.html`, as a background command)

2. Open `http://127.0.0.1:8766/index.html` in the browser

3. Measure the `.a4-page` element's actual height via JavaScript:
   ```javascript
   const page = document.querySelector('.a4-page');
   const scrollH = page.scrollHeight;
   const clientH = page.clientHeight;
   console.log(JSON.stringify({scrollHeight: scrollH, clientHeight: clientH, overflows: scrollH > clientH}));
   ```
   - A4 pixel height at 96dpi ≈ **1123px**
   - `scrollHeight > clientHeight` → content overflows
   - `clientHeight - scrollHeight > 80` → excessive whitespace

4. Take a screenshot for verification

> ⚠️ **Do NOT wait on HTTP server shutdown!** After verification, proceed immediately to the next step. Leave the HTTP server running in the background. Do NOT call `send_command_input` to terminate it — this causes long blocking delays.

### 2.5.2 Adaptive Layout Degradation Strategy

If content **overflows** (scrollHeight > clientHeight), apply the following degradation levels **one at a time**, re-verifying after each adjustment:

| Priority | Action | Description |
|----------|--------|-------------|
| **L1** | Merge education entries into single lines | Combine each education entry (school, major, date) into one line; move secondary info (advisor/direction) inline or omit |
| **L2** | Section-level column layout | For sections with multiple sub-headings (e.g., "Achievements & Honors"), add `section-Ncol` class to `.section-content`, where N = number of sub-items. 2 items → `section-2col`, 3 items → `section-3col` |
| **L3** | Reduce padding/margin | Shrink `.a4-page` padding (minimum `10mm 13mm`), section/item margins |
| **L4** | Reduce font size | Freely adjust while maintaining visual hierarchy. Minimum: **10pt** |
| **L5** | Prompt the user | If L4 still overflows, stop adjusting and suggest: "Content is too dense for a single-page resume. Consider using the multi-page template." |

> 🔒 **Line-height (≥ 1.5) does NOT participate in degradation. Never reduce it.**

If content has **excessive whitespace** (clientHeight - scrollHeight > 80px), apply the reverse:
- Increase font sizes and margins for better visual balance
- Goal: visually full but not crowded

### 2.5.3 Parameter Ranges Summary

| Parameter | Default | Minimum | Maximum |
|-----------|---------|---------|---------|
| body font-size | (dynamic) | 10pt | 13pt |
| line-height | 1.5 | 1.5 | 1.8 |
| .a4-page padding | 12mm 15mm | 10mm 13mm | 14mm 16mm |

**Step 3: Execute the Builder Script**
Run the core python compiler script provided in this repository to render the HTML into a perfect A4 PDF.
`$env:PYTHONIOENCODING = 'utf-8'; python builder.py index.html -o output_resume.pdf`

> ⚠️ **Windows encoding note**: You MUST set `PYTHONIOENCODING=utf-8` environment variable when running `builder.py` on Windows. Otherwise, emoji characters in console output will trigger a GBK encoding error.
>
> On Linux/macOS, simply run: `python builder.py index.html -o output_resume.pdf`

**Step 4: Verification and Clean-up**
1. Check if `output_resume.pdf` has been successfully generated.
2. Provide the file path to the user and notify them of the successful generation.

## 🚨 Critical Constraints
- **No Markdown**: The intermediate format MUST be written to an `.html` file.
- **DOM Rigidity**: Do not skip wrapper divs like `.section-content`. CSS selectors depend on this exact hierarchy.
- **Overflow Guard**: `max-height: 297mm; overflow: hidden;` on `.a4-page` is a safety net. Do NOT remove it.
- **Line-Height Floor**: 🔒 Line-height minimum is 1.5. Never reduce it.
- **Font Floor**: Never set body font-size below 10pt.
