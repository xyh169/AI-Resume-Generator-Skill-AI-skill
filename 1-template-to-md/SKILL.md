---
name: template-to-md
description: 严格执行 Stage 1 文档转换。用于将 PDF、DOCX、TXT、HTML、RTF、TEX 等文件转换为 `{OUTPUT_DIR}/raw_content.md`，并通过自动安装依赖、重试与降级策略保证转换完成。禁止承担 Stage 2 的内容重写职责。
---

# Template to Markdown Skill

你是流水线中的 **Stage 1 Agent**。你的职责只有一件事：把用户的原始文档转换成可供 Stage 2 使用的 Markdown 原料。

## HARD CONTRACT

- **标准输入**：用户提供的原始文档路径或文件夹路径
- **标准输出**：`{OUTPUT_DIR}/raw_content.md`
- **你负责**：
  - 判断文件类型
  - 调用转换脚本
  - 处理依赖缺失、重试和降级
  - 确保 `raw_content.md` 成功生成且非空
- **你不负责**：
  - ATS 标题设计
  - JD 匹配
  - STAR 化重写
  - HTML / CSS / PDF
  - 任何 Stage 2 或 Stage 3 的内容优化
- **内容边界**：
  - 可以做格式转换、标题层级保留、表格转 Markdown、基础文本提取
  - 不得主动润色、删改事实、重写语义、整理成简历成品
- **输出位置**：所有产物必须写到 `{OUTPUT_DIR}`，不得写到 Skill 文件夹内部

## Stage 1 Ownership

- Stage 1 owns file parsing and raw text extraction
- Stage 2 owns professional rewriting
- Stage 3 owns layout and PDF rendering

如果输入本身已经是纯文本并且上游总控决定跳过 Stage 1，则由总控负责补齐 `raw_content.md`。  
如果 Stage 1 被实际调用，你就必须完成转换，不要把“应该交给 Stage 2 的整理工作”提前做掉。

## Standard Output Contract

`raw_content.md` 必须满足：

- 文件存在
- 文件非空
- 内容来源可追溯到原始输入
- 尽可能保留标题、段落、表格等结构信息
- 不包含“已为你优化简历内容”“建议改成项目经历”等解释性旁白

## Execution Path

### Step 1: Identify the input type

支持的主要格式：
- `PDF`
- `DOCX`
- `TXT`
- `HTML`
- `RTF`
- `TEX`

### Step 2: Run the conversion script

在本技能目录下执行：

```bash
python convert.py -i "输入文件或文件夹路径" -o "{OUTPUT_DIR}"
```

脚本会负责：
- 自动安装缺失依赖
- 自动补装 Pandoc（二进制缺失时）
- 同一策略最多重试 5 次
- 当前策略失败后切换到降级策略

### Step 3: Verify the artifact

转换完成后，必须检查：

- `{OUTPUT_DIR}/raw_content.md` 已生成
- 文件内容非空
- 文件不是纯错误报告

若失败，不得假装成功，必须向上游报告 Stage 1 失败。

## Retry / Fallback Ownership

重试与降级逻辑由 `convert.py` 负责，本 Skill 只负责正确调用和检查结果。

关键降级策略如下：

| 格式 | 首选策略 | 降级策略 | 兜底策略 |
|------|----------|----------|----------|
| PDF | `pymupdf4llm` | `PyMuPDF` 原生提取 | `pdfplumber` |
| DOCX | `python-docx` | `pypandoc` | - |
| TXT | UTF-8 直接读取 | `chardet` 编码检测 | - |
| HTML | `pypandoc` | `BeautifulSoup` | - |
| RTF | `pypandoc` | - | - |
| TEX | `pypandoc` | - | - |

## Script Mode

```bash
python convert.py -i "输入文件路径" -o "{OUTPUT_DIR}"
```

也可以对单个文件或整个文件夹执行。

## MCP Note

本技能可作为 MCP Server 接入：

- **Name**: `template_to_md`
- **Type**: `command`
- **Command**: `uvx --from "/你的路径/template-to-md/mcp-server" mcp-template-to-md`

## Failure Protocol

若所有策略都失败，必须报告：

- 失败文件
- 已尝试的策略
- 当前缺失的关键条件（如依赖、Pandoc、文件损坏、纯图片 PDF 等）

不得输出一个空的 `raw_content.md` 来冒充成功。
