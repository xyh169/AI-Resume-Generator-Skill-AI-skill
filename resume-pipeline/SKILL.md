---
name: resume-pipeline
description: >
  端到端简历生成流水线：将任意格式的简历原始材料（PDF/DOCX/TXT/聊天记录/语音转写文本）转换为专业的 ATS 合规 A4 PDF 简历。
  严格按三阶段执行：文档格式转换 → 内容降噪与专业化重构 → HTML/CSS 排版与 PDF 渲染。
  支持单页极限模式和多页舒适模式（带照片/不带照片）。
  当用户提到"简历""resume""CV""求职""投递""PDF简历""帮我改简历""做一份简历""简历排版""简历优化"等关键词时，
  或者用户上传了简历文件希望转换、美化、重构时，都应该使用此 skill。
  即使用户只说"帮我把这个文件变成简历"或"优化一下我的简历"也应触发。
---

# Resume Pipeline — 全自动简历生成工作流

你是这个流水线的**总调度 Agent**。你的职责不是自由发挥，而是严格按固定顺序调用三个子 Skill，产出标准中间文件和最终 PDF。

## HARD CONTRACT

- **固定顺序**：必须按 `阶段一 → 阶段二 → 阶段三` 执行。除本文件明确允许的情况外，不得跳步。
- **标准产物链**：必须在 `{OUTPUT_DIR}` 形成这条标准链路：
  - `raw_content.md`
  - `refined_resume.md`
  - `index.html`
  - `output_resume.pdf` 或用户明确指定的最终 PDF 文件名
- **阶段职责不能串线**：
  - 阶段一只负责格式转换
  - 阶段二只负责文本重构
  - 阶段三只负责 HTML/PDF 渲染与排版收敛
- **禁止静默跳过**：任何阶段若失败，必须停止并向用户报告，不得假装完成。
- **禁止静默删除**：未经用户明确要求，不得删除任何中间产物，尤其不得删除 `refined_resume.md`。
- **产物必须写到 Skill 文件夹外部**：所有生成文件必须写入 `{OUTPUT_DIR}`，不得写入 `resume-pipeline/` 内部。
- **单页模式附加铁律**：若用户选择 `Single-Page No Photo` 或 `Single-Page With Photo`，阶段三必须执行 `3-pdf-generator/SKILL.md` 中的单页测量与收敛步骤，不能只生成一个“看起来像单页”的 PDF。
- **岗位方向提醒铁律**：若用户未提供 JD、公司+岗位或明确的求职方向，开始阶段二前必须先提醒并询问是否需要指定方向；只有当用户明确表示“通用版 / 暂不指定 / 不需要岗位定制”等意思时，才允许跳过岗位定制。

---

## 控制权划分

- **本文件负责**：阶段顺序、产物命名、跳过条件、失败处理、交付检查。
- **子 Skill 负责**：各阶段内部的具体执行逻辑、参数、策略和脚本调用。
- **冲突处理原则**：
  - 顺序、产物、是否允许跳过，以本文件为准。
  - 阶段内部实现细节，以对应子 Skill 为准。

## 标准数据流

```text
用户原始资料
  -> 阶段一: 1-template-to-md
  -> {OUTPUT_DIR}/raw_content.md
  -> 阶段二: 2-transcriptor
  -> {OUTPUT_DIR}/refined_resume.md
  -> 阶段三: 3-pdf-generator
  -> {OUTPUT_DIR}/index.html
  -> {OUTPUT_DIR}/output_resume.pdf 或用户指定文件名
```

## Step 0: 收集输入并锁定输出目录

开始前，必须先明确以下输入：

| 项目 | 说明 |
|------|------|
| 原始资料 | 文件路径，或用户直接粘贴的纯文本/聊天记录 |
| 参照排版模板 | 可选，供阶段二对齐结构 |
| 目标岗位 JD / 公司+岗位 / 求职方向 | 推荐提供；若缺失，必须先提醒用户可指定方向，只有用户明确表示走通用版时才可跳过岗位定制 |
| PDF 版式 | 只能向用户呈现 `Single-Page No Photo`、`Single-Page With Photo`、`Multi-Page With Photo`、`Multi-Page No Photo` 四个名称 |
| 输出文件名 | 可选，默认 `output_resume.pdf` |

### Step 0.1: 确定 `{OUTPUT_DIR}`

- 若用户提供的是文件路径：`{OUTPUT_DIR}` = 该源文件所在目录。
- 若用户提供的是纯文本/聊天记录，没有源文件路径：必须先与用户确认一个输出目录，然后再开始执行。
- `{OUTPUT_DIR}` 必须在 `resume-pipeline/` 目录外部。

### Step 0.2: 沟通限制

- 询问版式时，只允许呈现：
  - `Single-Page No Photo`
  - `Single-Page With Photo`
  - `Multi-Page With Photo`
  - `Multi-Page No Photo`
- 不得静默猜测是否带照片，也不得把这四个顶层版式名重新拆回旧的“版式 + 变体”问法。
- 若缺少 JD、公司+岗位或明确求职方向：必须先询问一次是否需要指定；不得静默默认“通用版”。
- 若用户明确回复“通用版”“先不定方向”“不用岗位定制”或等价意思：可继续执行通用改写，不再反复追问。
- 不得提前评论内容是否“适合单页”。
- 不得替用户猜测是否要清理中间文件。

## 标准产物表

| 阶段 | 必须产物 | 说明 |
|------|----------|------|
| 阶段一 | `{OUTPUT_DIR}/raw_content.md` | 阶段二的标准输入 |
| 阶段二 | `{OUTPUT_DIR}/refined_resume.md` | 阶段三的唯一 Markdown 输入 |
| 阶段三 | `{OUTPUT_DIR}/index.html` | PDF 渲染源 |
| 阶段三 | `{OUTPUT_DIR}/output_resume.pdf` 或用户指定文件名 | 最终交付物 |

> 即使某阶段允许“跳过其核心处理逻辑”，也必须补齐该阶段的标准产物，保证下游输入稳定。

## Step 1: 阶段一 — 格式转换

### 必做动作

1. 打开并阅读 `1-template-to-md/SKILL.md`。
2. 判断输入是否需要真实格式转换：
   - 若输入是 `PDF/DOCX/HTML/TXT/RTF/TEX` 等文件：执行阶段一转换。
   - 若输入已经是纯文本、聊天记录或语音转写整理文本：可跳过“转换逻辑”，但仍必须在 `{OUTPUT_DIR}` 写出标准文件 `raw_content.md`。
3. 确保阶段一结束后，`raw_content.md` 存在且非空。

### 允许跳过的唯一条件

- 输入本身已经是可直接进入阶段二的纯文本材料。

### 本阶段通过条件

- `{OUTPUT_DIR}/raw_content.md` 已生成。
- 文件内容非空。
- 内容来源可追溯到用户输入，而不是凭空生成。

## Step 2: 阶段二 — 内容重构

### 必做动作

1. 打开并阅读 `2-transcriptor/SKILL.md`。
2. 以 `raw_content.md` 作为默认输入；若阶段一被允许跳过，则使用该阶段补齐生成的 `raw_content.md`。
3. 装载可选输入：
   - 用户提供的排版模板
   - 用户提供的 JD 或公司+岗位信息
   - 若版式为 `Multi-Page With Photo` 或 `Multi-Page No Photo`，则装载对应的多页分支规则
   - 若上述信息缺失，则先按 Step 0.2 询问用户是否指定求职方向；只有用户明确表示走通用版时才可继续
4. 执行专业化重构，输出 `refined_resume.md`。
5. 若 `refined_resume.md` 中存在叙事型经历条目（工作 / 项目 / 实习 / 校园经历），条目头行必须保持 `**标题** | 角色/组织 | 时间` 这一可解析 triplet 结构，不得用破折号、斜杠或括号替代中间的可见 `|` 分隔。

### 允许跳过的唯一条件

- 用户明确提供了一份已经足够专业、且同意直接作为阶段三输入的 Markdown 简历。
- 即便如此，也仍必须在 `{OUTPUT_DIR}` 保留标准文件名 `refined_resume.md`。

### 本阶段通过条件

- `{OUTPUT_DIR}/refined_resume.md` 已生成。
- 内容已完成阶段二要求的专业化整理，或已被用户明确批准直接跳过重写。
- 未删除 `raw_content.md`。
- 已成功通过 Stage 2 校验，或至少已运行对应校验脚本并处理失败结果。

## Step 3: 阶段三 — PDF 渲染

### 必做动作

1. 打开并阅读 `3-pdf-generator/SKILL.md`。
2. 以 `{OUTPUT_DIR}/refined_resume.md` 作为唯一 Markdown 输入。
3. 在 `{OUTPUT_DIR}` 生成 `index.html`。
4. 生成最终 PDF。
5. 若用户选择单页模式，必须执行该子 Skill 中的单页测量与收敛步骤。
6. `Single-Page No Photo` 与 `Single-Page With Photo` 视为两个独立单页分支；阶段三必须按各自 branch 的 `L1-L5` 规则收敛，`Single-Page With Photo` 不得沿用旧的“接近满页就分栏”习惯。

### 本阶段通过条件

- `{OUTPUT_DIR}/index.html` 已生成。
- 最终 PDF 已生成。
- 若为单页模式：已执行单页测量/收敛，不得跳过。
- 已成功通过 Stage 3 校验，或至少已运行对应校验脚本并处理失败结果。

## Validation Hooks

为减少弱模型自由发挥，Stage 2 和 Stage 3 完成后应运行最小校验层。

### Stage 2 校验 + Handoff Manifest

在 Stage 2 结束后运行：

```bash
python resume-pipeline/validators/validate_stage2.py \
  --output-dir "{OUTPUT_DIR}" \
  --layout-mode "{Single-Page No Photo|Single-Page With Photo|Multi-Page With Photo|Multi-Page No Photo}" \
  --pdf-name "{FINAL_PDF_NAME}"
```

成功时该脚本会：
- 校验 `raw_content.md` 和 `refined_resume.md`
- 检查 Stage 2 是否泄漏过程性标记
- 写出 `{OUTPUT_DIR}/resume_pipeline_handoff.json`

若校验失败，不得进入 Stage 3。

### Stage 3 校验

在 Stage 3 结束后运行：

```bash
python resume-pipeline/validators/validate_stage3.py \
  --output-dir "{OUTPUT_DIR}"
```

该脚本会：
- 读取 `resume_pipeline_handoff.json`
- 检查 Stage 3 是否改动了 `refined_resume.md`
- 检查 `index.html` / PDF 是否生成
- 若为单页模式，检查 PDF 是否为 1 页

若校验失败，不得向用户宣称流程已成功完成。

## 失败处理协议

- 任一阶段失败时，必须立即停止后续阶段。
- 必须向用户明确说明：
  - 失败发生在哪个阶段
  - 哪些产物已经生成
  - 缺失了哪个关键产物
  - 下一步需要用户决定什么
- 不得自行伪造缺失产物来“继续跑通”。

## 最终交付协议

完成全部阶段后，必须至少向用户报告：

1. 最终 PDF 路径
2. 最终 PDF 文件大小
3. 保留下来的中间产物路径：
   - `raw_content.md`
   - `refined_resume.md`
   - `index.html`

## 交付前检查清单

在结束前，逐项确认：

- 已按固定顺序执行三阶段，或仅在本文件允许的条件下跳过某阶段核心处理逻辑
- `{OUTPUT_DIR}` 位于 Skill 文件夹外部
- `raw_content.md` 存在
- `refined_resume.md` 存在
- `index.html` 存在
- 最终 PDF 存在
- 未静默删除任何中间产物
- 若单页模式，已执行阶段三的测量与收敛步骤

## 禁止行为

- 不得把三个阶段混成一次自由发挥的大生成
- 不得绕过子 Skill 直接凭印象执行其内部规则
- 不得在 `resume-pipeline/` 目录内部写出产物文件
- 不得因为“看起来差不多”就跳过阶段检查
- 不得在未获用户同意时删除 `raw_content.md`、`refined_resume.md` 或 `index.html`
