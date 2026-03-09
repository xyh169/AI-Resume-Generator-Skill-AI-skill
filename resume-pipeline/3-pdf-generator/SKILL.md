---
name: Generate Blue-Purple Flag Resume
description: An end-to-end automated workflow for Antigravity, Cursor, and other Agentic AIs to digest any user document and generate a perfectly formatted, page-break-proof A4 PDF resume in either single-page or multi-page layouts.
---

# Blue-Purple Resume Workflow Skill

You are an expert AI Assistant tasked with converting a user's raw, unstructured profile (from a Word document, TXT, or chat history) into a professionally designed, A4-ready PDF resume.

## Prerequisites & Environment
1. Ensure Python 3 is installed and available in the terminal.
2. Ensure the required packages are installed by running:
   `pip install -r resources/requirements.txt`
3. Ensure Playwright browser binaries are present:
   `playwright install chromium`

## Workflow Steps

**Step 1: Understand User Requirements**
- Identify the source material (the user's unstructured text, DOCX, etc.).
- Identify the user's preferred layout: `Single-Page Extreme` (uses `resources/template_1page.css`) or `Multi-Page Comfortable` (uses `resources/template_multipage.css`). If not specified, ask the user or default to `Multi-Page Comfortable`.

**Step 2: Generate the HTML Structure**
You must act as the CSS/DOM architect and generate an `index.html` file in the current directory.
1. Read the exact content of the chosen CSS file (`resources/template_1page.css` or `resources/template_multipage.css`) from this repository.
2. Extract the user's professional information and map it strictly to the following DOM structure. DO NOT invent new classes.
3. **Dynamic Font-Size Injection**: The CSS template does NOT preset `font-size`. You must determine appropriate font sizes based on content volume and inject them into the `<style>` block.

### Font & Typography Rules

- **Global Font-Family**: You MUST override the default `font-family` in the CSS to prioritize English Arial and Chinese Microsoft YaHei/SimSun. Inject this rule into the `body` selector: `font-family: Arial, "Microsoft YaHei", "微软雅黑", SimSun, "宋体", sans-serif;`
- **Dynamic Font-Size**: The CSS template does NOT preset `font-size`. You must determine appropriate font sizes based on content volume.
- **Clear hierarchy**: Each level should be visually smaller than the one above (even 0.5pt difference is sufficient).
- **Minimum floor**: The smallest body font-size must not go below **9.5pt**.
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
        /* THEN INJECT font-size RULES AND font-family OVERRIDE */
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
            <!-- 3 sub-items → section-3col (equal) or section-3col-unequal (non-equal grid) -->
            <div class="section-content section-3col-unequal">
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

3. ⚠️ **Critical: Correct Measurement Method**

   The `.a4-page` element has `min-height: 297mm` and `overflow: hidden`, which means naive `scrollHeight` vs `clientHeight` comparison will **always return 0 gap** — the `min-height` props up the element and `overflow: hidden` clips the content. You **MUST** temporarily remove these constraints to get the true content height:

   ```javascript
   const el = document.querySelector('.a4-page');
   // Remove constraints to measure real content height
   el.style.overflow = 'visible';
   el.style.maxHeight = 'none';
   el.style.minHeight = '0';
   el.style.height = 'auto';
   const contentHeight = el.scrollHeight;
   const a4Height = 1123; // A4 at 96dpi
   const gap = a4Height - contentHeight;
   const usage = (contentHeight / a4Height * 100).toFixed(1);
   console.log(JSON.stringify({ contentHeight, a4Height, gap, usage: usage + '%' }));
   ```

   ❌ **DO NOT** use this broken approach (it always returns gap=0):
   ```javascript
   // WRONG — min-height inflates scrollHeight, overflow clips it
   const scrollH = el.scrollHeight;
   const clientH = el.clientHeight;  // Always equals scrollH!
   ```

4. Interpret the measurement result:
   - **`usage` in 90%–98%** → ✅ Ideal. Proceed to Step 3.
   - **`usage` < 85%** → Too much whitespace. Apply **Expansion Strategy** (see 2.5.3).
   - **`usage` > 100%** → Content overflows. Apply **Degradation Strategy** (see 2.5.2).
   - **`usage` in 85%–90%** → Acceptable but can be improved. Try light expansion.

> ⚠️ **Do NOT wait on HTTP server shutdown!** After verification, proceed immediately to the next step. Leave the HTTP server running in the background. Do NOT call `send_command_input` to terminate it — this causes long blocking delays.

### 2.5.2 Adaptive Layout Degradation Strategy (Overflow → Shrink)

If content **overflows** (usage > 100%), apply the following degradation levels **one at a time**, re-verifying after each adjustment:

| Priority | Action | Description |
|----------|--------|-------------|
| **L1** | Merge education entries into single lines | Combine each education entry (school, major, date) into one line; move secondary info (advisor/direction) inline or omit |
| **L2** | Section-level column layout | For sections with multiple sub-headings, add `section-Ncol` class to `.section-content`. 2 items → `section-2col`, 3 items → `section-3col` (equal columns), or `section-3col-unequal` (first column wider) |
| **L3** | Reduce padding/margin | Shrink `.a4-page` padding (minimum `10mm 13mm`), section/item margins |
| **L4** | Reduce font size | Freely adjust while maintaining visual hierarchy. Minimum: **9.5pt** |
| **L5** | Prompt the user | If L4 still overflows, stop adjusting and suggest: "Content is too dense for a single-page resume. Consider using the multi-page template." |

> 🔒 **Line-height (≥ 1.5) does NOT participate in degradation. Never reduce it.**

### 2.5.3 Expansion Strategy (Excessive Whitespace → Enlarge)

If content has **excessive whitespace** (usage < 85%), you must enlarge to fill the page. Apply the following **in combination**, not one-at-a-time, then re-verify:

| Priority | Action | Description | Typical Impact |
|----------|--------|-------------|----------------|
| **E1** | Increase body font-size | +0.5–1pt per round | ~30–60px per step |
| **E2** | Increase line-height | Up to 1.8 maximum | ~40–80px across full page |
| **E3** | Increase padding | Up to `14mm 16mm` | ~30–50px total |
| **E4** | Increase section/item margins | `section-title` margin, `.item` margin-bottom, `.section-content` margin-bottom | ~20–40px total |
| **E5** | Increase title font sizes | h1 up to 22pt, h2 up to 14pt, item-title up to 12pt | ~10–20px total |

**⚠️ Expansion Pitfall: Avoid Overshoot**

Expanding is trickier than shrinking — font-size and line-height have a **multiplicative effect** (they compound across every line of text). A seemingly small change from `9pt → 10.5pt` body + `1.35 → 1.6` line-height can push usage from 76% to 112% in one step.

**Recommended approach:**
1. **First round**: Adjust body font-size by +0.5pt AND increase line-height to 1.5 (if below). This alone often adds ~100px.
2. **Re-measure.** If still < 90%, do a second round: +0.3pt font AND slightly increase padding/margins.
3. **Never change more than 2 parameters at once** — it's easy to overshoot.

### 2.5.4 Iterative Convergence Loop

The adjustment process is iterative. Expect 2–3 rounds to converge on the ideal 90–95% usage:

```
Round 1: Measure → Adjust → Re-measure
Round 2: Fine-tune → Re-measure
Round 3: (if needed) Micro-adjust → Final confirmation
```

**Target: 90%–95% usage is the sweet spot.** This leaves a small visual margin at the bottom without looking empty.

### 2.5.5 Parameter Ranges Summary

| Parameter | Default | Minimum | Maximum | Impact |
|-----------|---------|---------|---------|--------|
| body font-size | 9.8pt (typical) | 9.5pt | 13pt | HIGH — affects every line |
| line-height | 1.5 | 1.5 | 1.8 | HIGH — affects every line |
| .a4-page padding | 12mm 15mm | 10mm 13mm | 14mm 16mm | MEDIUM |
| h1 font-size | 16pt | 14pt | 22pt | LOW |
| h2 font-size | 12pt | 11pt | 14pt | LOW |
| item-title font-size | 10.5pt | 9.5pt | 12pt | LOW-MEDIUM |
| .item margin-bottom | 4px | 2px | 8px | LOW-MEDIUM |
| .section-title margin | 5px 0 4px 0 | 3px 0 2px 0 | 8px 0 6px 0 | LOW |

### 2.5.6 Quick-Start Parameter Presets

Based on empirical testing, here are recommended starting points by content volume:

| Content Volume | body font | line-height | padding | h1 | h2 | item-title |
|---------------|-----------|-------------|---------|----|----|------------|
| **Light** (3–4 sections, <15 bullet points) | 11pt | 1.6 | 12mm 15mm | 18pt | 13pt | 11pt |
| **Medium** (5–6 sections, 15–25 bullets) | 9.8pt | 1.5 | 10mm 14mm | 16pt | 12pt | 10.5pt |
| **Heavy** (6+ sections, 25+ bullets) | 9.5pt | 1.5 | 10mm 13mm | 16pt | 11pt | 9.5pt |

These are starting points — always verify with the measurement script and iterate.

**Step 3: Execute the Builder Script**
Run the core python compiler script provided in this repository to render the HTML into a perfect A4 PDF.
`$env:PYTHONIOENCODING = 'utf-8'; python scripts/builder.py index.html -o output_resume.pdf`

> ⚠️ **Windows encoding note**: You MUST set `PYTHONIOENCODING=utf-8` environment variable when running `builder.py` on Windows. Otherwise, emoji characters in console output will trigger a GBK encoding error.
>
> On Linux/macOS, simply run: `python scripts/builder.py index.html -o output_resume.pdf`

**Step 4: Verification and Clean-up**
1. Check if `output_resume.pdf` has been successfully generated.
2. Provide the file path to the user and notify them of the successful generation.

## 🚨 Critical Constraints
- **No Markdown**: The intermediate format MUST be written to an `.html` file.
- **DOM Rigidity**: Do not skip wrapper divs like `.section-content`. CSS selectors depend on this exact hierarchy.
- **Overflow Guard**: `max-height: 297mm; overflow: hidden;` on `.a4-page` is a safety net. Do NOT remove it.
- **Line-Height Floor**: 🔒 Line-height minimum is 1.5. Never reduce it.
- **Font Floor**: Never set body font-size below 9.5pt.
- **Measurement Correctness**: Always remove `min-height`, `max-height`, and `overflow` before measuring real content height. Failure to do so will return a fake gap of 0.
- **Target Fill Rate**: Aim for 90%–95% page usage. Below 85% looks empty; above 98% risks content clipping.
- **Iterative Convergence**: Expect 2–3 measurement rounds. Never assume a single adjustment will be correct. Always re-measure after changes.
- **Multiplicative Caution**: `font-size` and `line-height` have multiplicative effects — a small change applies to every line and compounds quickly. Adjust incrementally (+0.3–0.5pt per round).
