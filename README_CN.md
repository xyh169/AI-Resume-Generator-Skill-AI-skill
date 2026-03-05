# AI Resume Generator Skill | AI 简历自动生成Skill

<p align="center">
  <b>🌏 Language / 语言</b><br>
  <a href="./README.md">English</a> | <a href="./README_CN.md">简体中文</a>
</p>

> 一个 AI 原生的、精心打造的 A4 简历框架。将你的零散笔记转化为令人惊艳的 PDF 简历。

这是一个通过 AI 将任意非结构化文本（如闲聊记录、Word、TXT），转化为具备完美打印排版（防分页截断、高度兼容 1~N 页）的 A4 PDF 简历全套开源工作流。

## 🎯 核心功能
- **AI 赋能转化**：包含特制的超级 System Prompt，能够一键教导大语言模型提取关键信息，输出严格契合本 CSS 样式的跨页 HTML。
- **自适应多页裁剪**：完美解决了 HTML 转 PDF 中长列表断尾、大面积留白的问题，保障任何一页长出或切断都拥有原生物理级完美留白。
- **原生一键渲染**：搭配 Playwright 的 headless 生成管线，确保在终端零配置一键导出 A4。

## 📦 文件目录说明
- `prompt_workflow.md`: 喂给大模型（如 Cursor / Claude / ChatGPT）的超级 Prompt（也叫 AI Skill），把你的个人经历丢给它，它就能吐出完美的底层 HTML。
- `template_1page.css`: 单页 A4 适用模板，专为需要用一页纸向外企、投行投递而设计，空间利用率拉到顶峰。
- `template_multipage.css`: 舒适展开的多页长篇模板，自带完美的 20mm 大留白与物理分页保护，多少长度都会自然跨界排版。
- `builder.py`: Python 主程序，用于渲染并固化导出 PDF。
- `requirements.txt`: Python 运行依赖。

## 🚀 极简使用指南

> **环境强要求**: 本项目依靠 Python 进行后端无头浏览器渲染。所以请确保你的电脑上安装了 `Python 3.8+`。

### 方式 A：Agent 智能全自动流（强烈推荐 ✨）
如果你正在使用 `Antigravity`、`Cursor`、`Codex` 或 `Claude Code` 等 AI 编程助手软件，你**完全不需要**自己动手配置和运行！只需要在当前目录跟 AI 说一段"咒语"：

> *"请阅读我的旧简历，调用这里的 `SKILL.md`，使用 [多页版]（或 [单页版]）为我重新生成一份名为 `my_new_resume.pdf` 的精美简历并自动执行所有环境配置命令。"*

AI 助手便会自动读取库里的 `SKILL.md`，替你完成理解、抓取 CSS、写 HTML、配置 Python 依赖并运行脚本的全套流程，直接把一份现成的 PDF 交由你手中！

### 方式 B：手动单机执行模式
*适合无智能型 AI 在旁，只依赖标准版 ChatGPT 网页生成 HTML 的情况。*

**Step 1: 准备内容**
打开任意网页版 AI（如 ChatGPT），将本级目录下的 `prompt_workflow.md` 内容发给它，并要求【单页极限版】或【多页舒适版】，获取自动编写的 `resume.html` 文件。

### Step 2: 安装依赖
```bash
pip install -r requirements.txt
playwright install chromium
```

### Step 3: 出图
将 AI 吐出的 `resume.html` 放在本目录下，并运行：
```bash
python builder.py resume.html
```
你将直接在此目录下收获一份 `resume.pdf`，带有无瑕疵的多页自动跨行防截断蓝紫旗帜排版！

---

## ✨ v1.1.0 更新日志

- **自适应单页排版引擎**：新增 Step 2.5 浏览器溢出检测 + 5 级渐进式降级策略（L1–L5），自动依次执行行合并 → 大模块分栏 → 缩 padding → 缩字号 → 提示用户。
- **动态字号注入**：单页版本CSS 模板不再预设 `font-size`，由 AI 根据内容量自行决定最优字号，保持清晰的视觉层级（`h1 >> h2 > item-title ≥ body`，底线：10pt）。
- **Section 级分栏布局**：新增 `.section-2col` / `.section-3col` CSS 类，对含多个次级标题的大模块整体分栏，栏数 = 次级标题数。
- **行距铁律**：行距锁定 ≥ 1.5，不参与任何降级操作。
- **Windows 编码修复**：新增 `PYTHONIOENCODING=utf-8` 环境变量说明，避免 Windows 上的 GBK 编码错误。
- **无阻塞验证服务器**：HTTP 验证服务器改为"用完即弃"模式，避免关闭服务器时的长时间阻塞。

---

## 📄 许可证
GLP-3.0
