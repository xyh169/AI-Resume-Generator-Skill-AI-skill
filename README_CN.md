# Resume Pipeline - 全自动简历生成工作流

<p align="center">
  <b>Language / 语言</b><br>
  <a href="README.md">English</a> | 简体中文
</p>

> 一个基于 Agent 的端到端简历流水线。无论输入是 Word、PDF、HTML、纯文本，还是口语化的聊天记录与语音转写，都可以被整理为结构化内容，并渲染成专业的 A4 PDF 简历。

## 核心架构与能力概览

整个工作流由三个阶段按固定顺序组成，覆盖从原始资料解析到最终 PDF 渲染的完整流程。

| 阶段 | 核心模块 | 主要能力 |
|------|---------|---------|
| **1** | `1-template-to-md` | 负责格式转换与原始内容提取。支持 `PDF`、`DOCX`、`TXT`、`HTML`、`RTF`、`TEX` 等格式，也能接收聊天记录或语音转写。内置重试与降级策略。 |
| **2** | `2-transcriptor` | 负责内容重构与专业化表达。根据目标岗位或 JD 做匹配，按 ATS 兼容结构输出 `refined_resume.md`。叙事型条目头部会保持稳定格式，例如 `**项目名** | 角色 | 时间`。 |
| **3** | `3-pdf-generator` | 负责 HTML/CSS 排版与 PDF 导出。支持 `Single-Page Extreme`、`Single-Page Photo`，以及 `Multi-Page Comfortable` 的 `With Photo` / `No Photo` 两种变体。单页模式使用浏览器测量与收敛，多页模式使用共享跨页规则。 |

## 目录结构

```text
├── README.md                -> 英文说明
├── README_CN.md             -> 中文说明
└── resume-pipeline/         -> 核心流水线目录
    ├── SKILL.md             -> 总控入口
    ├── REFACTOR_PLAN.md     -> 重构计划
    ├── 1-template-to-md/    -> 阶段一：格式转换
    ├── 2-transcriptor/      -> 阶段二：内容重构
    ├── 3-pdf-generator/     -> 阶段三：排版渲染与 PDF 导出
    ├── references/          -> 各分支 reference
    └── validators/          -> 阶段校验脚本
```

## v2.3.0 更新日志

这次版本主要更新了带照片的单页模板。

- **带照片的单页模板更新**：`Single-Page Photo` 调整为专用的顶部照片壳层结构。左侧放姓名、横排基本信息与教育经历，右侧放固定一寸照片位，下面再回到正常的单栏正文流。
- **头部衔接感优化**：补充了照片头部左栏的对齐规则，让“姓名 + 基本信息 + 教育经历”更贴近照片行下沿，减轻与下方正文模块之间的分裂感。


---

## 历史更新存档

### v2.2.0

- **全链路 Skill 合同化收紧**：总控与三个阶段 Skill 增加了显式 `HARD CONTRACT`、阶段职责、标准产物、通过条件与失败处理，减少串阶段和自由发挥。
- **最小校验层 + Handoff Manifest**：新增 Stage 2 / Stage 3 校验器，并生成 `resume_pipeline_handoff.json`，用于检查关键产物、过程标记泄漏以及单页 PDF 是否真的只有一页。
- **Stage 3 reference 拆分**：将单页、多页与多页变体规则拆到独立 reference 中，主 `SKILL.md` 主要承担路由与合同职责。
- **多页版双变体**：`Multi-Page Comfortable` 明确拆为 `With Photo` 与 `No Photo` 两种变体。
- **内容感知型蓝色引导竖线**：优化多页版竖线逻辑，使其跟随真实内容块而不是机械拉满。
- **单页内容门槛重校准**：调整 Stage 2 的单页预检阈值，减少对可读内容的过度压缩。
- **单页 handoff 说明补充**：进一步明确 Stage 2 到 Stage 3 的 Markdown 交接要求。

### v2.1.0

- **ATS 兼容标准标题**：增加中英文 ATS 标准 section 标题映射表。
- **排版逻辑顺序优化**：完善单页模式的降级、扩展与闭环验证流程。
- **用户参数引导更清晰**：明确顶层版式选择与多页变体选择。
- **Section 内容类型标注**：加入 `<!-- type: narrative -->` 与 `<!-- type: data -->` 约定，供 Stage 3 识别。

### v2.0.0

- **从单脚本升级为三阶段流水线**：形成 `template-to-md -> transcriptor -> pdf-generator` 的完整协作链路。
- **扩展输入格式**：支持 PDF、DOCX、TXT、HTML、RTF、TEX 以及非结构化聊天文本。
- **原生支持 MCP**：可作为 MCP server 接入支持相关协议的 AI IDE 或 Agent 环境。

### v1.1.0

- **自适应单页布局引擎**：加入浏览器测量与单页收敛策略。
- **动态字号注入**：根据内容体量自动确定字号层级。
- **Section 级分栏支持**：引入 `.section-2col` / `.section-3col` 等布局类。
- **行高安全下限**：保证行高不低于 `1.5`。

## 版式选择流程

1. 先选择 `Single-Page Extreme`、`Single-Page Photo` 或 `Multi-Page Comfortable`。
2. 如果选择 `Multi-Page Comfortable`，再选择 `With Photo` 或 `No Photo`。
3. 如果没有提供 JD / 公司+岗位 / 求职方向，工作流会先追问一次，再决定是否走通用版。

## 推荐使用方式

### 方案 A：AI Agent 全自动模式

在支持 Agent 的 IDE 或应用中，可以直接使用类似下面的提示词：

> 请阅读 `resume-pipeline/SKILL.md`，使用我提供的原始资料（附件、文本）帮我生成一份简历。目标岗位是 [公司名 + 岗位名 / 具体 JD]，请按 `Single-Page Extreme`、`Single-Page Photo` 或 `Multi-Page Comfortable` 渲染；如果是多页版，再选择 `With Photo` 或 `No Photo`。

如果提供了目标岗位信息，工作流会做岗位匹配与内容定制；如果没有提供，工作流会先询问是否需要指定方向。单页模式下，Stage 3 会自动执行测量与收敛，而不是只输出一个“看起来像单页”的 PDF。

### 方案 B：作为 MCP 服务接入

如果你的环境支持 MCP，可以将底层能力直接挂载为独立服务。以 Cursor 为例：

- `convert_file_to_md`：`uvx --from "/你的绝对路径/1-template-to-md/mcp-server" mcp-template-to-md`
- `transcriptor-agent`：`uvx --from "/你的绝对路径/2-transcriptor/mcp-server" mcp-transcriptor`

更多执行协议和系统提示词配置，请分别阅读各子目录中的 `SKILL.md`。

---

## 许可证

GPL-3.0
