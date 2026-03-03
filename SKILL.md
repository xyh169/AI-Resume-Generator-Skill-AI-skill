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

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        /* INJECT THE ENTIRE CHOSEN CSS HERE */
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
    </div>
</body>
</html>
```

**Step 3: Execute the Builder Script**
Run the core python compiler script provided in this repository to render the HTML into a perfect A4 PDF.
`python builder.py index.html -o output_resume.pdf`

**Step 4: Verification and Clean-up**
1. Check if `output_resume.pdf` has been successfully generated.
2. Provide the file path to the user and notify them of the successful generation.

## 🚨 Critical Constraints
- **Absolute CSS Fidelity**: You MUST inject the exact, unmodified CSS from the chosen template file into the `<style>` block.
- **No Markdown**: The intermediate format MUST be written to an `.html` file.
- **DOM Rigidity**: Do not skip wrapper divs like `.section-content`. The CSS selectors depend on this exact hierarchy.
