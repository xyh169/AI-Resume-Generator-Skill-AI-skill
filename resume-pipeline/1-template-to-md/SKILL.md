---
name: template-to-md
description: 基于 MCP 协议的文档格式转换工具，支持 PDF/DOCX/HTML 等转 Markdown。具备自动安装依赖、错误重试（最多5次）、多策略降级转换能力。
---

# MCP: Template to Markdown Skill (v2.0 增强版)

文档格式转换为 Markdown 的技能包，支持单机脚本和 MCP Server 两种使用方式。

## v2.0 新增能力

- **自动安装依赖**: 缺少 Python 库时自动 `pip install`，缺少 Pandoc 二进制时自动下载
- **错误重试**: 同一转换策略最多重试 5 次，每次失败后自动修复再重试
- **多策略降级**: 主策略失败后自动切换备选方案（例如 PDF: pymupdf4llm → PyMuPDF 原生 → pdfplumber）
- **截断机制**: 5 次重试仍失败则切换策略；所有策略耗尽后输出详细错误报告，建议用户手动处理
- **增强 DOCX**: 保留标题层级（Heading 1-6 → `# ~ ######`），提取表格为 Markdown 格式
- **编码自动检测**: TXT 文件 UTF-8 失败时自动使用 chardet 检测编码
- **HTML 降级**: pypandoc 失败时自动切换 BeautifulSoup 提取

### 各格式降级策略一览

| 格式 | 策略 1 (首选) | 策略 2 (降级) | 策略 3 (兜底) |
|------|--------------|--------------|--------------|
| PDF  | pymupdf4llm  | PyMuPDF 原生  | pdfplumber   |
| DOCX | python-docx  | pypandoc     | -            |
| TXT  | UTF-8 直接读取 | chardet 编码检测 | -         |
| HTML | pypandoc     | BeautifulSoup | -           |
| RTF  | pypandoc     | -            | -            |
| TEX  | pypandoc     | -            | -            |

## 方案一：基础 Python 脚本执行

进入技能包根目录运行:

```bash
# 直接运行（依赖会在运行时自动安装）
python convert.py -i "输入文件夹路径" -o "输出文件夹路径"

# 也可以转换单个文件
python convert.py -i "某个文件.pdf" -o "输出文件夹"
```

> 注意：首次运行某种格式时如果缺少依赖，脚本会自动安装，可能需要等待几秒钟。

## 方案二：作为 MCP Server 接入 AI 客户端

此技能内置 MCP Server 服务代码。通过配置给 Cursor / Claude Desktop，AI 可直接调用 `convert_file_to_md` 解析文档。

### 前提条件

系统全局安装 `uv` 包管理器:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Cursor 接入方式

1. Cursor → Settings → Features → MCP
2. 点击 "+ Add New MCP Server"
3. 填入:
   - **Name**: `template_to_md`
   - **Type**: `command`
   - **Command**: `uvx --from "/你的路径/template-to-md/mcp-server" mcp-template-to-md`

配置完成后，AI 即可自动调用文档转换能力，遇到错误会自动重试和降级。
