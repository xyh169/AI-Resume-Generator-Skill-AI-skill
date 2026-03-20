"""
Resume Pipeline — 统一 MCP Server

将整个简历流水线（格式转换 → 内容重构 → PDF 渲染）封装为一个符合 MCP 协议的服务。

暴露的 MCP 原语：
  Tools     — convert_file_to_md, render_html_to_pdf,
              validate_stage2, validate_stage3, run_pipeline
  Resources — CSS 模板、排版参考文档、流水线规范
  Prompts   — resume_rewrite_guidelines, pipeline_briefing
"""

import json
import os
import subprocess
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# 定位项目根目录（mcp-server/ 的上一层就是 resume-pipeline/）
# ---------------------------------------------------------------------------
_THIS_DIR = Path(__file__).resolve().parent                     # src/mcp_resume_pipeline/
_MCP_SERVER_DIR = _THIS_DIR.parent.parent                       # mcp-server/
_PROJECT_ROOT = _MCP_SERVER_DIR.parent                          # resume-pipeline/
_STAGE1_DIR = _PROJECT_ROOT / "1-template-to-md"
_STAGE3_DIR = _PROJECT_ROOT / "3-pdf-generator"
_VALIDATORS_DIR = _PROJECT_ROOT / "validators"
_RESOURCES_DIR = _STAGE3_DIR / "resources"
_REFERENCES_DIR = _STAGE3_DIR / "references"

# ---------------------------------------------------------------------------
# FastMCP 实例
# ---------------------------------------------------------------------------
mcp = FastMCP(
    "Resume Pipeline",
    description=(
        "简历全流水线 MCP 服务：文档格式转换 → 内容专业化重构 → A4 PDF 渲染。"
        "提供 Tools（转换、渲染、校验、全流程执行）、Resources（CSS 模板、排版参考）"
        "和 Prompts（重写指南、流水线简报）。"
    ),
)

# ===================================================================
#  TOOLS
# ===================================================================

# ---- Stage 1: 文档转 Markdown ----

# 复用 Stage 1 已有的转换引擎（直接 import，避免代码重复）
sys.path.insert(0, str(_STAGE1_DIR))
try:
    from convert import process_file as _stage1_process_file
except ImportError:
    _stage1_process_file = None


@mcp.tool()
def convert_file_to_md(file_path: str) -> str:
    """将本地文档转换为 Markdown。

    支持格式：.pdf, .docx, .txt, .html, .htm, .rtf, .tex
    内置自动依赖安装、错误重试（最多 5 次）、多策略降级。

    Args:
        file_path: 目标文档的绝对路径（如 /Users/.../resume.pdf）

    Returns:
        转换后的 Markdown 文本。全部策略失败时返回详细错误报告。
    """
    if not os.path.exists(file_path):
        return f"[错误] 文件不存在: {file_path}"

    if _stage1_process_file is None:
        return (
            "[错误] 无法加载 Stage 1 转换引擎 (1-template-to-md/convert.py)。"
            "请确认项目结构完整。"
        )

    return _stage1_process_file(file_path)


# ---- Stage 3: HTML → PDF 渲染 ----

@mcp.tool()
def render_html_to_pdf(
    html_path: str,
    output_path: str = "",
    format: str = "A4",
) -> str:
    """使用 Playwright (Chromium) 将 HTML 简历渲染为 PDF。

    Args:
        html_path:   输入 HTML 文件的绝对路径
        output_path: 输出 PDF 路径（默认与输入同目录同名 .pdf）
        format:      纸张格式，默认 A4

    Returns:
        成功时返回 PDF 路径与文件大小；失败时返回错误信息。
    """
    builder_script = _STAGE3_DIR / "scripts" / "builder.py"
    if not builder_script.exists():
        return f"[错误] 找不到渲染脚本: {builder_script}"

    if not os.path.exists(html_path):
        return f"[错误] HTML 文件不存在: {html_path}"

    cmd = [sys.executable, str(builder_script), html_path]
    if output_path:
        cmd.extend(["-o", output_path])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            return f"[错误] PDF 渲染失败:\n{result.stderr or result.stdout}"

        # 解析实际输出路径
        actual_output = output_path or (os.path.splitext(html_path)[0] + ".pdf")
        if os.path.exists(actual_output):
            size_kb = os.path.getsize(actual_output) / 1024
            return (
                f"[成功] PDF 已生成\n"
                f"路径: {actual_output}\n"
                f"大小: {size_kb:.2f} KB"
            )
        return f"[警告] 渲染过程无报错但未找到输出文件: {actual_output}\n{result.stdout}"
    except subprocess.TimeoutExpired:
        return "[错误] PDF 渲染超时（120 秒）"
    except Exception as e:
        return f"[错误] 渲染异常: {e}"


# ---- Validators ----

@mcp.tool()
def validate_stage2(
    output_dir: str,
    layout_mode: str = "Single-Page Extreme",
    multi_page_variant: str = "not_required",
    pdf_name: str = "output_resume.pdf",
    content_volume: str = "",
) -> str:
    """运行 Stage 2 校验，检查 raw_content.md 和 refined_resume.md 的完整性与合规性。

    成功时会在 output_dir 生成 resume_pipeline_handoff.json 交接清单。

    Args:
        output_dir:          包含 raw_content.md 和 refined_resume.md 的目录
        layout_mode:         版式模式 ("Single-Page Extreme" 或 "Multi-Page Comfortable")
        multi_page_variant:  多页变体 ("With Photo" / "No Photo" / "not_required")
        pdf_name:            预期最终 PDF 文件名
        content_volume:      可选的内容量标签 ("light" / "medium" / "heavy")

    Returns:
        JSON 格式的校验结果报告。
    """
    script = _VALIDATORS_DIR / "validate_stage2.py"
    if not script.exists():
        return f"[错误] 校验脚本不存在: {script}"

    cmd = [
        sys.executable, str(script),
        "--output-dir", output_dir,
        "--layout-mode", layout_mode,
        "--multi-page-variant", multi_page_variant,
        "--pdf-name", pdf_name,
    ]
    if content_volume:
        cmd.extend(["--content-volume", content_volume])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.stdout or result.stderr
    except Exception as e:
        return f"[错误] 校验执行异常: {e}"


@mcp.tool()
def validate_stage3(output_dir: str, manifest_path: str = "") -> str:
    """运行 Stage 3 校验，检查 index.html 和 PDF 产物是否完整。

    会读取 resume_pipeline_handoff.json 以对比 refined_resume.md 哈希，
    确认 Stage 3 没有擅自修改内容。

    Args:
        output_dir:     包含所有产物的目录
        manifest_path:  可选的 handoff manifest 显式路径

    Returns:
        JSON 格式的校验结果报告。
    """
    script = _VALIDATORS_DIR / "validate_stage3.py"
    if not script.exists():
        return f"[错误] 校验脚本不存在: {script}"

    cmd = [sys.executable, str(script), "--output-dir", output_dir]
    if manifest_path:
        cmd.extend(["--manifest", manifest_path])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.stdout or result.stderr
    except Exception as e:
        return f"[错误] 校验执行异常: {e}"


@mcp.tool()
def run_pipeline(
    input_path: str,
    output_dir: str,
    layout_mode: str = "Single-Page Extreme",
    multi_page_variant: str = "not_required",
    pdf_name: str = "output_resume.pdf",
) -> str:
    """执行完整的三阶段简历流水线：格式转换 → 内容保存 → PDF 渲染。

    注意：Stage 2（内容重构）需要 LLM 交互，本 tool 仅自动完成 Stage 1 和 Stage 3
    的机械操作。Stage 2 的重写应由调用方 Agent 根据 resume_rewrite_guidelines prompt
    来完成，然后将结果写入 {output_dir}/refined_resume.md 后再调用此 tool 的 Stage 3
    部分，或分别调用各阶段 tool。

    此 tool 的典型用法是：作为 Agent 调度的辅助，快速完成非 LLM 部分。

    Args:
        input_path:         源文件路径（PDF/DOCX/TXT 等）或已有 raw_content.md 路径
        output_dir:         所有产物的输出目录
        layout_mode:        版式模式
        multi_page_variant: 多页变体
        pdf_name:           最终 PDF 文件名

    Returns:
        各阶段执行状态的汇总报告。
    """
    report_lines = []
    os.makedirs(output_dir, exist_ok=True)

    # === Stage 1: 格式转换 ===
    raw_md_path = os.path.join(output_dir, "raw_content.md")

    # 如果输入本身已经是 raw_content.md，跳过转换
    if input_path.endswith("raw_content.md") and os.path.exists(input_path):
        if os.path.abspath(input_path) != os.path.abspath(raw_md_path):
            import shutil
            shutil.copy2(input_path, raw_md_path)
        report_lines.append("[Stage 1] 输入已是 raw_content.md，跳过转换。")
    elif os.path.exists(input_path):
        md_content = convert_file_to_md(input_path)
        if md_content.startswith("[错误]"):
            report_lines.append(f"[Stage 1] 失败: {md_content}")
            return "\n".join(report_lines)
        with open(raw_md_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        report_lines.append(f"[Stage 1] 完成 → {raw_md_path}")
    else:
        report_lines.append(f"[Stage 1] 失败: 输入文件不存在 {input_path}")
        return "\n".join(report_lines)

    # === Stage 2: 需要 LLM 交互，此处仅检查 ===
    refined_md_path = os.path.join(output_dir, "refined_resume.md")
    if os.path.exists(refined_md_path):
        report_lines.append(f"[Stage 2] 检测到已有 refined_resume.md，跳过（假设由 Agent 完成）。")
    else:
        report_lines.append(
            "[Stage 2] 等待中 — refined_resume.md 尚未生成。"
            "请由 Agent 参考 resume_rewrite_guidelines prompt 完成内容重构，"
            "将结果写入 " + refined_md_path + " 后再继续。"
        )
        return "\n".join(report_lines)

    # === Stage 2 Validation ===
    v2_result = validate_stage2(output_dir, layout_mode, multi_page_variant, pdf_name)
    try:
        v2_json = json.loads(v2_result)
        if not v2_json.get("valid"):
            report_lines.append(f"[Stage 2 校验] 失败: {v2_json.get('failures', [])}")
            return "\n".join(report_lines)
        report_lines.append("[Stage 2 校验] 通过 ✓")
    except (json.JSONDecodeError, TypeError):
        report_lines.append(f"[Stage 2 校验] 输出: {v2_result}")

    # === Stage 3: HTML → PDF ===
    # Stage 3 需要 Agent 先生成 index.html，这里检查是否存在
    html_path = os.path.join(output_dir, "index.html")
    if not os.path.exists(html_path):
        report_lines.append(
            "[Stage 3] 等待中 — index.html 尚未生成。"
            "请由 Agent 根据 refined_resume.md 和 CSS 模板资源生成 index.html，"
            "然后调用 render_html_to_pdf 工具完成 PDF 渲染。"
        )
        return "\n".join(report_lines)

    pdf_output = os.path.join(output_dir, pdf_name)
    render_result = render_html_to_pdf(html_path, pdf_output)
    report_lines.append(f"[Stage 3] {render_result}")

    # === Stage 3 Validation ===
    v3_result = validate_stage3(output_dir)
    try:
        v3_json = json.loads(v3_result)
        if not v3_json.get("valid"):
            report_lines.append(f"[Stage 3 校验] 失败: {v3_json.get('failures', [])}")
        else:
            report_lines.append("[Stage 3 校验] 通过 ✓")
    except (json.JSONDecodeError, TypeError):
        report_lines.append(f"[Stage 3 校验] 输出: {v3_result}")

    return "\n".join(report_lines)


# ===================================================================
#  RESOURCES — 暴露 CSS 模板、排版参考文档和流水线规范
# ===================================================================

@mcp.resource("resume://templates/css/1page")
@mcp.resource("resume://templates/css/single-page")
def get_css_single_page() -> str:
    """单页极限模式的 CSS 模板 (template_1page.css)"""
    css_path = _RESOURCES_DIR / "template_1page.css"
    return css_path.read_text(encoding="utf-8") if css_path.exists() else "[资源缺失]"


@mcp.resource("resume://templates/css/1page_photo")
@mcp.resource("resume://templates/css/single-page-photo")
def get_css_single_page_photo() -> str:
    """Single-page photo CSS template (template_1page_photo.css)"""
    css_path = _RESOURCES_DIR / "template_1page_photo.css"
    return css_path.read_text(encoding="utf-8") if css_path.exists() else "[missing resource]"


@mcp.resource("resume://templates/css/multipage")
@mcp.resource("resume://templates/css/multipage-with-photo")
def get_css_multipage_photo() -> str:
    """多页带照片模式的 CSS 模板 (template_multipage.css)"""
    css_path = _RESOURCES_DIR / "template_multipage.css"
    return css_path.read_text(encoding="utf-8") if css_path.exists() else "[资源缺失]"


@mcp.resource("resume://templates/css/multipage-2")
@mcp.resource("resume://templates/css/multipage-no-photo")
def get_css_multipage_no_photo() -> str:
    """多页无照片模式的 CSS 模板 (template_multipage-2.css)"""
    css_path = _RESOURCES_DIR / "template_multipage-2.css"
    return css_path.read_text(encoding="utf-8") if css_path.exists() else "[资源缺失]"


@mcp.resource("resume://references/single-page-mode")
def get_ref_single_page() -> str:
    """单页收敛排版参考文档"""
    ref_path = _REFERENCES_DIR / "single-page-mode.md"
    return ref_path.read_text(encoding="utf-8") if ref_path.exists() else "[资源缺失]"


@mcp.resource("resume://references/single-page-photo-mode")
def get_ref_single_page_photo() -> str:
    """Single-page photo layout reference"""
    ref_path = _REFERENCES_DIR / "single-page-photo-mode.md"
    return ref_path.read_text(encoding="utf-8") if ref_path.exists() else "[missing resource]"


@mcp.resource("resume://references/multi-page-mode")
def get_ref_multi_page() -> str:
    """多页排版参考文档"""
    ref_path = _REFERENCES_DIR / "multi-page-mode.md"
    return ref_path.read_text(encoding="utf-8") if ref_path.exists() else "[资源缺失]"


@mcp.resource("resume://references/multi-page-with-photo")
def get_ref_multi_page_photo() -> str:
    """多页带照片排版参考文档"""
    ref_path = _REFERENCES_DIR / "multi-page-with-photo-mode.md"
    return ref_path.read_text(encoding="utf-8") if ref_path.exists() else "[资源缺失]"


@mcp.resource("resume://references/multi-page-no-photo")
def get_ref_multi_page_no_photo() -> str:
    """多页无照片排版参考文档"""
    ref_path = _REFERENCES_DIR / "multi-page-no-photo-mode.md"
    return ref_path.read_text(encoding="utf-8") if ref_path.exists() else "[资源缺失]"


@mcp.resource("resume://references/prompt-workflow")
def get_ref_prompt_workflow() -> str:
    """Stage 3 渲染工作流参考"""
    ref_path = _RESOURCES_DIR / "prompt_workflow.md"
    return ref_path.read_text(encoding="utf-8") if ref_path.exists() else "[资源缺失]"


@mcp.resource("resume://spec/pipeline")
def get_pipeline_spec() -> str:
    """流水线总规范 (SKILL.md)"""
    spec_path = _PROJECT_ROOT / "SKILL.md"
    return spec_path.read_text(encoding="utf-8") if spec_path.exists() else "[资源缺失]"


# ===================================================================
#  PROMPTS — 暴露可复用的提示模板
# ===================================================================

@mcp.prompt()
def resume_rewrite_guidelines(has_jd: bool = False, keyword: str = "") -> str:
    """获取专业的简历重写与结构化降噪指南。

    Agent 在执行 Stage 2（内容重构）时必须先获取此 prompt 并遵循其规则。

    Args:
        has_jd:  用户是否已提供明确的 JD（职位描述）
        keyword: 用户指定的目标公司或岗位关键词
    """
    base = """# 简历降噪与专业化重构铁律

你是一个专业的猎头与文档架构师，必须对用户提供的漫谈式简历执行以下动作，输出极其标准格式的 Markdown 文件。

## Step 1: 降噪、清洗与语言专业化

所有的口语内容必须在这个阶段被转化为具有高商业价值的职业化话术。

- **不能捏造**：只能做减法（去除无用废话、情绪表达）和重构（整理从句、提炼逻辑），绝不替用户捏造原本不存在的数据与成果。
- **摒弃弱势口语**：
  - 不可接受: "我弄出来了"、"我大概从 x 年都在干这个"
  - 应当改为: "主导研发"、"独立负责"、"全流程跟进"
- **信息抽屉法**：将荣誉丢进荣誉板块，专利丢进专利板块，不要混杂在常规项目里。
- **STAR 法则补齐**：情境背景 + 核心动作 + 定量/定性结果。

## Step 2: 格式要求

请仔细对齐要求的排版模块（头衔栏、教育背景、工作/实习经历、项目经历、成果与荣誉），通过加粗关键指标进行高亮。
禁止输出无意义的换行符或多个空行。保持页面紧凑。

## Step 3: ATS 合规

- 使用标准 section 标题（如：教育背景、工作经历、项目经历、专业技能、荣誉奖项）
- 为每个 section 添加类型注解（`<!-- type: narrative -->` 或 `<!-- type: data -->`）
- 禁止在输出中遗留任何过程性标记（如 content_volume:、给下游排版器、TODO）
"""
    if has_jd:
        base += (
            "\n\n## 定制化强化要求\n\n"
            "用户已提供了目标求职岗位的 JD。请在重塑项目经历时，"
            "重点**提炼并加粗**与该岗位核心要求最匹配的工具、业务场景或能力。"
            "边缘经历可极度弱化。"
        )
    elif keyword:
        base += (
            f"\n\n## 定制化强化要求\n\n"
            f"用户想针对【{keyword}】的岗位投递。请先确认该方向的招聘核心要求，"
            f"并在改写简历时针对性优化用词。"
        )

    return base


@mcp.prompt()
def pipeline_briefing(
    layout_mode: str = "Single-Page Extreme",
    multi_page_variant: str = "not_required",
) -> str:
    """获取流水线执行简报，供 Agent 快速了解当前配置下的执行流程。

    Args:
        layout_mode:        版式模式
        multi_page_variant: 多页变体（仅多页模式需要）
    """
    asset_map = {
        ("Single-Page Extreme", "not_required"): {
            "css_file": "template_1page.css",
            "css_resource": "resume://templates/css/single-page",
            "ref_file": "single-page-mode.md",
            "ref_resource": "resume://references/single-page-mode",
        },
        ("Single-Page Photo", "not_required"): {
            "css_file": "template_1page_photo.css",
            "css_resource": "resume://templates/css/single-page-photo",
            "ref_file": "single-page-photo-mode.md",
            "ref_resource": "resume://references/single-page-photo-mode",
        },
        ("Multi-Page Comfortable", "With Photo"): {
            "css_file": "template_multipage.css",
            "css_resource": "resume://templates/css/multipage-with-photo",
            "ref_file": "multi-page-mode.md",
            "ref_resource": "resume://references/multi-page-mode + resume://references/multi-page-with-photo",
        },
        ("Multi-Page Comfortable", "No Photo"): {
            "css_file": "template_multipage-2.css",
            "css_resource": "resume://templates/css/multipage-no-photo",
            "ref_file": "multi-page-mode.md",
            "ref_resource": "resume://references/multi-page-mode + resume://references/multi-page-no-photo",
        },
    }
    assets = asset_map.get(
        (layout_mode, multi_page_variant),
        asset_map[("Single-Page Extreme", "not_required")],
    )
    css_file = assets["css_file"]
    css_resource = assets["css_resource"]
    ref_file = assets["ref_file"]
    ref_resource = assets["ref_resource"]

    return f"""# 流水线执行简报

## 当前配置
- 版式模式: {layout_mode}
- 多页变体: {multi_page_variant}
- CSS 模板: {css_file}
- 排版参考: {ref_file}

## 执行流程

### Stage 1: 格式转换
调用 `convert_file_to_md` tool 将源文件转为 Markdown。
产物: {{OUTPUT_DIR}}/raw_content.md

### Stage 2: 内容重构
1. 先调用 `resume_rewrite_guidelines` prompt 获取重写规则
2. 根据规则对 raw_content.md 进行专业化重构
3. 输出写入 {{OUTPUT_DIR}}/refined_resume.md
4. 调用 `validate_stage2` tool 校验

### Stage 3: PDF 渲染
1. 读取 resource `resume://templates/css/{css_file.replace('.css', '').replace('template_', '')}` 获取 CSS
2. 读取 resource `resume://references/{ref_file.replace('.md', '')}` 获取排版参考
3. 根据 refined_resume.md + CSS 生成 index.html
4. 调用 `render_html_to_pdf` tool 渲染 PDF
5. 调用 `validate_stage3` tool 校验

## 铁律提醒
- 固定顺序: Stage 1 → Stage 2 → Stage 3，不可跳步
- Stage 3 不得修改 refined_resume.md 的内容
- 单页模式必须执行浏览器测量与收敛
- 所有产物必须写入 OUTPUT_DIR（Skill 文件夹外部）
"""


# ===================================================================
#  入口
# ===================================================================

def main():
    mcp.run()


if __name__ == "__main__":
    main()
