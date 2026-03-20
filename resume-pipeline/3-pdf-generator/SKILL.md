---
name: blue-purple-pdf-generator
description: 严格执行 Stage 3 排版与 PDF 渲染。用于把 `refined_resume.md` 转换为固定 DOM 的 `index.html` 并生成 A4 PDF；单页模式下必须执行浏览器测量与收敛。禁止承担 Stage 2 的文本重写职责，除本技能明确允许的极少量版式型文本重排外，不得改写简历语义内容。
---

# Blue-Purple Resume Workflow Skill

You are the **Stage 3 Agent** in the resume pipeline. Your job is to take the finalized Markdown resume and turn it into a professionally rendered A4 HTML/PDF output.

## HARD CONTRACT

- **Standard input**: `{OUTPUT_DIR}/refined_resume.md`
- **Standard outputs**:
  - `{OUTPUT_DIR}/index.html`
  - `{OUTPUT_DIR}/output_resume.pdf` or the user-specified final PDF name
- **You are responsible for**:
  - choosing the correct CSS template
  - choosing the correct multi-page variant when applicable
  - mapping Markdown content into the fixed DOM structure
  - injecting typography/layout parameters
  - single-page measurement and convergence when required
  - running the builder and verifying the PDF
- **You are NOT responsible for**:
  - JD matching
  - ATS section selection
  - substantive text rewriting
  - inventing or deleting resume facts
- **Allowed text change boundary**:
  - You may do minimal layout-preserving text normalization explicitly required by this skill, such as reflowing an education entry into a single line while preserving the same facts.
  - You must not add, fabricate, or semantically rewrite the candidate's content.
- **Single-page iron rule**: If the user chooses `Single-Page Extreme` or `Single-Page Photo`, you must execute the browser measurement and convergence flow. Do not skip it.
- **Output location**: All outputs must be written to `{OUTPUT_DIR}`, not inside the Skill folder.

## Stage 3 Ownership

- Stage 2 owns text restructuring and `refined_resume.md`
- Stage 3 owns layout, HTML generation, measurement, and PDF rendering
- If Stage 3 receives incomplete or clearly non-final Markdown, stop and report the issue instead of silently rewriting the content layer

## Reading Path

- **Multi-Page Comfortable**:
  - Read this file
  - Read `references/multi-page-mode.md`
  - If variant is `With Photo`, read `resources/template_multipage.css`, then read `references/multi-page-with-photo-mode.md`
  - If variant is `No Photo`, read `resources/template_multipage-2.css`, then read `references/multi-page-no-photo-mode.md`
  - Skip the single-page reference file
- **Single-Page Extreme**:
  - Read this file
  - Read `resources/template_1page.css`
  - Then read `references/single-page-mode.md`
  - Follow the measurement/convergence process there before rendering the PDF
- **Single-Page Photo**:
  - Read this file
  - Read `resources/template_1page_photo.css`
  - Then read `references/single-page-photo-mode.md`
  - Follow the measurement/convergence process there before rendering the PDF

## Prerequisites & Environment
1. Ensure Python 3 is installed and available in the terminal.
2. Ensure the required packages are installed by running:
   `pip install -r resources/requirements.txt`
3. Ensure Playwright browser binaries are present:
   `playwright install chromium`

## Workflow Steps

**Step 1: Understand User Requirements**
- Identify the source material (the user's unstructured text, DOCX, etc.).
- Accepted layout names are `Single-Page Extreme`, `Single-Page Photo`, and `Multi-Page Comfortable`.
- `Single-Page Photo` is a separate top-level layout and uses `resources/template_1page_photo.css`.
- Identify the user's preferred layout: `Single-Page Extreme` (uses `resources/template_1page.css`) or `Multi-Page Comfortable` (uses a multi-page template). If not specified, ask the user to choose — present only these two options by name, without making any judgment about whether the content will or won't fit in one page. Content feasibility is handled automatically by the pipeline; do not speculate about it.
- If the user selects `Multi-Page Comfortable`, identify the multi-page variant:
  - `With Photo` -> use `resources/template_multipage.css`
  - `No Photo` -> use `resources/template_multipage-2.css`
- If the user selects multi-page but does not specify the variant, ask a follow-up using only `With Photo` and `No Photo`.

**Step 2: Generate the HTML Structure**
You must act as the CSS/DOM architect and generate an `index.html` file in the output directory (`OUTPUT_DIR`, determined by the upstream Master Workflow — typically the directory where the user's source file resides, **outside** the Skill folder).
1. Read the exact content of the chosen CSS file (`resources/template_1page.css`, `resources/template_multipage.css`, or `resources/template_multipage-2.css`) from this repository.
   - For `Single-Page Photo`, use `resources/template_1page_photo.css`.
   - For `Multi-Page Comfortable + With Photo`, use `resources/template_multipage.css`.
   - For `Multi-Page Comfortable + No Photo`, use `resources/template_multipage-2.css`.
2. Extract the user's professional information and map it strictly to the following DOM structure. DO NOT invent new classes.
   - Exception: `Single-Page Photo` may use the dedicated wrapper classes defined in the variant skeleton below.
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

### Section 分类（用于后续分栏判断）

所有 section 按内容性质分为两类，**分类仅用于在单页测量阶段后决定是否分栏，初始生成时一律单栏**：

| 类型 | 包含的 Section | 特征 |
|------|---------------|------|
| **描述型** | 工作经历、项目经历、实习经历、校园经历、个人总结 | 每条 bullet 是长段落（STAR 描述），通常 40–120 字 |
| **数据型** | 科研成果、荣誉奖项、证书资质、专业技能、语言能力 | 每条是短条目（列数据），通常 10–40 字 |

> 教育背景有专用的 `.edu-item` 布局，不参与分栏分类。描述型 section **永远不分栏**，无论测量结果如何。

> 🔒 **分栏是测量后的补救手段，不是初始布局选择。Step 2 生成 HTML 时所有 section 均为单栏，只有进入单页测量/收敛流程后才按需启用分栏。**

### HTML Skeleton

> 🔒 **动态 Section 原则**：下方模板列出了所有可能的 section 类型。实际生成时，**只输出上游 Markdown 中实际存在的 section**。没有对应内容的 section 必须整块省略，不要输出空 section。Section 标题必须使用 ATS 兼容的标准标题（参见上游 `2-transcriptor` 的准则 0）。**初始生成时所有 section 均为单栏，不预先添加任何分栏 class。**

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
        <!-- ====== Header（必选） ====== -->
        <div class="header">
            <h1>姓名</h1>
            <p><strong>电话</strong>: ... | <strong>邮箱</strong>: ... | <strong>其他信息</strong>: ...</p>
        </div>

        <!-- ====== 多页版可选：基本信息 + 右侧照片（仅 Multi-Page Comfortable + With Photo） ====== -->
        <div class="section">
            <div class="section-title"><h2>基本信息</h2></div>
            <div class="section-content">
                <div class="basic-info-layout">
                    <div class="basic-info-grid">
                        <div class="basic-info-item"><span class="basic-info-label">性别</span><span>男 / 女</span></div>
                        <div class="basic-info-item"><span class="basic-info-label">学历</span><span>硕士 / 本科 / 博士</span></div>
                        <div class="basic-info-item"><span class="basic-info-label">政治面貌</span><span>中共党员 / 群众 / ...</span></div>
                        <div class="basic-info-item"><span class="basic-info-label">电话</span><span>13800000000</span></div>
                        <div class="basic-info-item"><span class="basic-info-label">邮箱</span><span>name@example.com</span></div>
                    </div>
                    <div class="photo-box"><img src="photo.jpg" alt="Profile photo"></div>
                    <!-- 若用户要求预留照片位但暂未提供照片，也可改用 <div class="photo-slot">照片</div> -->
                </div>
            </div>
        </div>
        <!-- Multi-Page Comfortable + No Photo: omit this entire block by default -->

        <!-- ====== 教育背景（必选） ====== -->
        <div class="section">
            <div class="section-title"><h2>教育背景</h2></div>
            <div class="section-content">
                <div class="item edu-item">
                    <div class="edu-header">
                        <div><span class="edu-school">学校名</span> | <span class="edu-major">专业</span><span class="edu-detail">学位</span></div>
                        <div class="item-date">起止时间</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ====== 个人总结（可选：有则写，无则省略整块） ====== -->
        <div class="section">
            <div class="section-title"><h2>个人总结</h2></div>
            <div class="section-content">
                <div class="item">
                    <ul>
                        <li><span class="k">亮点关键词</span>：概括性描述...</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- ====== 工作经历（可选） ====== -->
        <div class="section">
            <div class="section-title"><h2>工作经历</h2></div>
            <div class="section-content">
                <div class="item">
                    <div class="item-header">
                        <div><span class="item-title">职位</span><span class="item-org">| 公司</span></div>
                        <div class="item-date">起止时间</div>
                    </div>
                    <ul>
                        <li><span class="k">亮点关键词</span>：STAR 法则描述...</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- ====== 项目经历（可选） ====== -->
        <div class="section">
            <div class="section-title"><h2>项目经历</h2></div>
            <div class="section-content">
                <div class="item">
                    <div class="item-header">
                        <div><span class="item-title">项目名称</span><span class="item-org">| 角色</span></div>
                        <div class="item-date">起止时间</div>
                    </div>
                    <ul>
                        <li><span class="k">亮点关键词</span>：STAR 法则描述...</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- ====== 实习经历（可选） ====== -->
        <div class="section">
            <div class="section-title"><h2>实习经历</h2></div>
            <div class="section-content">
                <div class="item">
                    <div class="item-header">
                        <div><span class="item-title">公司名</span><span class="item-org">| 岗位</span></div>
                        <div class="item-date">起止时间</div>
                    </div>
                    <ul>
                        <li><span class="k">亮点关键词</span>：描述...</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- ====== 校园经历（可选） ====== -->
        <div class="section">
            <div class="section-title"><h2>校园经历</h2></div>
            <div class="section-content">
                <div class="item">
                    <div class="item-header">
                        <div><span class="item-title">组织名</span><span class="item-org">| 职位</span></div>
                        <div class="item-date">起止时间</div>
                    </div>
                    <ul>
                        <li><span class="k">亮点关键词</span>：描述...</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- ====== 专业技能（可选） ====== -->
        <div class="section">
            <div class="section-title"><h2>专业技能</h2></div>
            <div class="section-content">
                <div class="item">
                    <ul>
                        <li><span class="k">类别</span>：技能1、技能2、技能3</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- ====== 证书资质（可选） ====== -->
        <div class="section">
            <div class="section-title"><h2>证书资质</h2></div>
            <div class="section-content">
                <div class="item">
                    <ul>
                        <li>证书名称（发证机构，获得时间）</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- ====== 科研成果（可选） ====== -->
        <div class="section">
            <div class="section-title"><h2>科研成果</h2></div>
            <div class="section-content">
                <div class="item">
                    <ul>
                        <li>论文/专利描述...</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- ====== 荣誉奖项（可选） ====== -->
        <div class="section">
            <div class="section-title"><h2>荣誉奖项</h2></div>
            <div class="section-content">
                <div class="item">
                    <ul>
                        <li><span class="k">年份</span>：奖项名称</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- ====== 语言能力（可选） ====== -->
        <div class="section">
            <div class="section-title"><h2>语言能力</h2></div>
            <div class="section-content">
                <div class="item">
                    <ul>
                        <li>语种：水平/成绩</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- ====== Section-Level Column Layout Example ====== -->
        <!-- 当同一 section 下有多个并列子模块时，可用分栏布局节省空间 -->
        <!-- Column count = number of sub-items: 2 → section-2col, 3 → section-3col / section-3col-unequal -->
        <!--
        <div class="section">
            <div class="section-title"><h2>荣誉奖项</h2></div>
            <div class="section-content section-2col">
                <div class="item">子模块1...</div>
                <div class="item">子模块2...</div>
            </div>
        </div>
        -->
    </div>
</body>
</html>
```

### Single-Page Photo Layout Skeleton

When the user selects `Single-Page Photo`, use the dedicated **top-photo intro shell** below. Keep `.section`, `.section-title`, `.section-content`, and `.item` intact.

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        /* INJECT resources/template_1page_photo.css */
        /* THEN INJECT font-size RULES AND font-family OVERRIDE */
    </style>
</head>
<body>
    <div class="a4-page">
        <div class="single-page-photo-hero">
            <div class="single-page-photo-intro">
                <div class="header">
                    <h1>姓名</h1>
                </div>

                <div class="single-page-photo-basic-info">
                    <div class="single-page-photo-basic-line"><span class="single-page-photo-basic-label">电话</span><span class="single-page-photo-basic-value">13800000000</span></div>
                    <div class="single-page-photo-basic-line"><span class="single-page-photo-basic-label">邮箱</span><span class="single-page-photo-basic-value">name@example.com</span></div>
                    <div class="single-page-photo-basic-line"><span class="single-page-photo-basic-label">城市</span><span class="single-page-photo-basic-value">上海</span></div>
                </div>
                <!-- Personal info should stay on one horizontal line when width permits -->
                <!-- The whole left intro block should sit bottom-left in the hero row -->

                <div class="section">
                    <div class="section-title"><h2>教育背景</h2></div>
                    <div class="section-content">
                        <div class="edu-item">
                            <div class="edu-header">
                                <div><span class="edu-school">学校</span><span class="edu-major"> | 专业</span><span class="edu-detail"> | 学位</span></div>
                                <span class="item-date">时间</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="single-page-photo-aside">
                <div class="sidebar-photo">
                    <div class="photo-box"><img src="photo.jpg" alt="Profile photo"></div>
                </div>
            </div>
        </div>

        <!-- Render all remaining sections below in the normal single-column order -->
    </div>
</body>
</html>
```

### Multi-Page Comfortable Addendum

If the user selected `Multi-Page Comfortable`, you MUST read and follow:
- `references/multi-page-mode.md`
- If variant is `With Photo`, also read `references/multi-page-with-photo-mode.md`
- If variant is `No Photo`, also read `references/multi-page-no-photo-mode.md`

Use the shared multi-page reference file for:
- content-aware blue guide line rules
- page-break and cross-page constraints
- other multi-page-only shared constraints

### Single-Page Extreme Addendum

If the user selected `Single-Page Extreme`, you MUST read and follow:
- `references/single-page-mode.md`

Use the single-page reference file for:
- browser verification setup
- degradation / expansion / convergence flow
- target usage interpretation and stop conditions
- single-page-only layout guardrails

### Single-Page Photo Addendum

If the user selected `Single-Page Photo`, you MUST read and follow:
- `references/single-page-photo-mode.md`
- `references/single-page-mode.md`

Use the single-page photo reference file for:
- browser verification setup
- top intro with left-side name/basic-info/education plus right-side photo assembly
- bottom-left alignment of the left intro block inside the hero row
- photo-branch-specific `L1`-`L5` degradation semantics
- single-page-photo-only guardrails

Use the old single-page reference file for:
- degradation / expansion / convergence flow
- the old `L2` data-section column procedure
- parameter tuning ranges

`L2` guardrail for both single-page branches:
- If the page already fits on one page, do **not** apply `L2`.
- Do not split short data sections such as `Certifications` unless columnization is required to remove actual overflow.

Header text guardrail:
- Keep a visible `|` between `.item-title` and `.item-org` in narrative item headers; this separator belongs in the generated HTML text, not in CSS.

**Step 3: Execute the Builder Script**
Run the core python compiler script provided in this repository to render the HTML into a perfect A4 PDF.
`$env:PYTHONIOENCODING = 'utf-8'; python scripts/builder.py {OUTPUT_DIR}/index.html -o {OUTPUT_DIR}/output_resume.pdf`

> ⚠️ **Windows encoding note**: You MUST set `PYTHONIOENCODING=utf-8` environment variable when running `builder.py` on Windows. Otherwise, emoji characters in console output will trigger a GBK encoding error.
>
> On Linux/macOS, simply run: `python scripts/builder.py {OUTPUT_DIR}/index.html -o {OUTPUT_DIR}/output_resume.pdf`

**Step 4: Verification and Clean-up**
1. Check if `output_resume.pdf` has been successfully generated.
2. Provide the file path to the user and notify them of the successful generation.

## 🚨 Critical Constraints
- **No Markdown**: The intermediate format MUST be written to an `.html` file.
- **DOM Rigidity**: Do not skip wrapper divs like `.section-content`. CSS selectors depend on this exact hierarchy.
- **Overflow Guard**: `max-height: 297mm; overflow: hidden;` on `.a4-page` is a safety net. Do NOT remove it.
- **Text Integrity**: Do not semantically rewrite the resume content at Stage 3. Only minimal layout-preserving normalization explicitly allowed by this skill is permitted.
- **Line-Height Floor**: 🔒 Line-height minimum is 1.5. Never reduce it.
- **Font Floor**: Never set body font-size below 9.5pt.
- **Measurement Correctness**: Always remove `min-height`, `max-height`, and `overflow` before measuring real content height. Failure to do so will return a fake gap of 0.
- **Photo Header Shell**: For `Single-Page Photo`, only the top intro area is photo-aware. The body below must remain the usual single-column flow unless the old single-page degradation rules temporarily apply column helpers.
- **Reuse Old Degradation**: For `Single-Page Photo`, reuse the old `Single-Page Extreme` degradation and expansion rules instead of inventing a new sidebar balancing algorithm.
- **No Unnecessary L2**: If the page already fits, keep data sections single-column; `L2` is only for fixing real overflow.
- **Target Fill Rate**: Aim for 93%–98% page usage. Below 85% looks empty; above 98% risks content clipping.
- **Iterative Convergence**: Expect 2–3 measurement rounds. Never assume a single adjustment will be correct. Always re-measure after changes.
- **Text Encoding**: Literal labels such as `基本信息` and `照片位` must survive as valid UTF-8 text. Do not emit `?` placeholder glyphs for fixed labels.
- **Multiplicative Caution**: `font-size` and `line-height` have multiplicative effects — a small change applies to every line and compounds quickly. Adjust incrementally (+0.3–0.5pt per round).
- **Single-Page Branch Isolation**: `template_1page.css` + `references/single-page-mode.md` remain the old single-page branch. `template_1page_photo.css` + `references/single-page-photo-mode.md` are a separate single-page-with-photo branch. Do not merge or overwrite either branch.
- **Multi-Page Isolation**: Content-aware guide-line rules remain a **multi-page-only** update. Do not retrofit them into either single-page branch unless explicitly requested.
- **Multi-Page Variant Isolation**: `template_multipage.css` is the `With Photo` variant; `template_multipage-2.css` is the `No Photo` variant. Do not mix their DOM expectations.
