---
name: Resume Pipeline Master Workflow
description: 一键式简历生成全流程编排。自动串联"文档格式转换 → 内容专业化重构 → A4 PDF 渲染"三大阶段，将任意原始资料（Word/PDF/TXT/聊天记录）转化为精美的 Blue-Purple 旗帜风格 PDF 简历。
---

# Resume Pipeline — 全自动简历生成工作流

你是一个全自动简历生成流水线的总调度 Agent。本 Skill 将三个独立子 Skill 按固定顺序串联执行，实现从原始资料到成品 PDF 的端到端自动化。

## 数据流转总览

```
用户原始资料（Word/PDF/TXT/聊天记录）
        │
        ▼
  ┌──────────────────┐
  │ 阶段一：格式转换    │  1-template-to-md/SKILL.md
  │ (template-to-md)  │  PDF/DOCX/HTML/TXT → 纯文本 Markdown
  └──────────────────┘
        │ 产出：raw_content.md
        ▼
  ┌──────────────────┐
  │ 阶段二：内容重构    │  2-transcriptor/SKILL.md
  │ (transcriptor)    │  降噪 + STAR 法则 + 专业化改写
  └──────────────────┘
        │ 产出：refined_resume.md
        ▼
  ┌──────────────────┐
  │ 阶段三：PDF 渲染   │  3-pdf-generator/SKILL.md
  │ (pdf-generator)   │  Markdown → HTML → A4 PDF
  └──────────────────┘
        │ 产出：final_resume.pdf
```

---

## Workflow Steps

### Step 0: 收集用户输入

在启动流水线之前，向用户确认以下信息：

| 必需项 | 说明 |
|--------|------|
| **原始资料文件** | 用户提供的 Word/PDF/TXT 文件路径或粘贴的文本 |
| **参照排版模板**（可选） | 用于 transcriptor 阶段的 Markdown 排版模板文件 |
| **目标岗位 JD**（可选） | 用于定制化改写的岗位描述文本或公司+岗位名 |
| **PDF 版式** | `Single-Page Extreme`（单页极限版）或 `Multi-Page Comfortable`（多页舒适版），默认多页版 |
| **输出文件名**（可选） | 最终 PDF 的文件名，默认 `output_resume.pdf` |

---

### Step 1: 阶段一 — 格式转换（template-to-md）

**目标**：将用户提供的任意格式文档转换为纯文本 Markdown。

1. **读取子 Skill 指令**：打开并阅读 `1-template-to-md/SKILL.md`，按照其中的步骤执行。
2. **执行转换**：
   ```bash
   python 1-template-to-md/convert.py -i "用户文件路径" -o "临时输出目录"
   ```
3. **产出**：获得 `raw_content.md`（纯文本 Markdown 格式的简历内容）。
4. **阶段检查**：确认 `raw_content.md` 已成功生成且内容非空。

> ⚠️ 如果用户直接提供的是纯文本或聊天记录（无需格式转换），可**跳过本阶段**，直接进入阶段二。

---

### Step 2: 阶段二 — 内容重构（transcriptor）

**目标**：将格式转换后的原始 Markdown 进行专业化降噪与结构化重写。

1. **读取子 Skill 指令**：打开并阅读 `2-transcriptor/SKILL.md`，按照其中的步骤执行。
2. **装载输入**：
   - 原始内容：上一阶段产出的 `raw_content.md`
   - 排版模板（如用户提供）
   - 岗位 JD（如用户提供）
3. **执行重构**：按照 transcriptor 的四步流程（意图探测 → 装载标尺 → 降噪清洗 → 输出交付）。
4. **产出**：获得 `refined_resume.md`（专业化、结构化的 Markdown 简历）。
5. **阶段检查**：确认内容已完成专业化改写，无口语化表达残留。

---

### Step 3: 阶段三 — PDF 渲染（pdf-generator）

**目标**：将重构后的 Markdown 内容转化为 HTML，并渲染为完美的 A4 PDF。

1. **读取子 Skill 指令**：打开并阅读 `3-pdf-generator/SKILL.md`，按照其中的**全部步骤**执行（包括 Step 2.5 的浏览器溢出验证，如果是单页模式）。
2. **关键步骤**：
   - 读取对应的 CSS 模板（`3-pdf-generator/resources/template_1page.css` 或 `template_multipage.css`）
   - 基于 `refined_resume.md` 的内容生成 `index.html`
   - 动态注入字号（单页模式需执行自适应排版引擎）
   - 运行 `python 3-pdf-generator/scripts/builder.py index.html -o output_resume.pdf`
3. **产出**：获得最终的 `output_resume.pdf`。
4. **阶段检查**：确认 PDF 文件已生成，通知用户并提供文件路径。

---

### Step 4: 交付与清理

1. 向用户报告最终 PDF 的**文件路径**和**文件大小**。
2. （可选）询问用户是否需要清理中间产物（`raw_content.md`、`refined_resume.md`、`index.html`）。
3. （可选）询问用户是否需要微调（如切换单页/多页版式、调整内容）。

---

## 🚨 全局约束

- **严格顺序执行**：必须按 阶段一 → 阶段二 → 阶段三 的顺序执行，每个阶段的输出是下一个阶段的输入。
- **子 Skill 独立性**：每个阶段的具体逻辑以对应子目录的 `SKILL.md` 为准，本文件仅负责编排。详细的参数、策略表、铁律等请参见各子 Skill 内部文档。
- **阶段间可断点**：如果某个阶段失败，Agent 应报告错误并询问用户如何处理，而非强行跳过。
- **智能跳过**：如果用户输入已经是纯文本，可跳过阶段一；如果用户提供的 MD 已经足够专业，可与用户确认后跳过阶段二。
