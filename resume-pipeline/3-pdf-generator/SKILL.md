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
- Identify the user's preferred layout: `Single-Page Extreme` (uses `resources/template_1page.css`) or `Multi-Page Comfortable` (uses `resources/template_multipage.css`). If not specified, ask the user to choose — present only these two options by name, without making any judgment about whether the content will or won't fit in one page. Content feasibility is handled automatically by the pipeline; do not speculate about it.

**Step 2: Generate the HTML Structure**
You must act as the CSS/DOM architect and generate an `index.html` file in the output directory (`OUTPUT_DIR`, determined by the upstream Master Workflow — typically the directory where the user's source file resides, **outside** the Skill folder).
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

### Section 分类（用于后续分栏判断）

所有 section 按内容性质分为两类，**分类仅用于在 Step 2.5 测量后决定是否分栏，初始生成时一律单栏**：

| 类型 | 包含的 Section | 特征 |
|------|---------------|------|
| **描述型** | 工作经历、项目经历、实习经历、校园经历、个人总结 | 每条 bullet 是长段落（STAR 描述），通常 40–120 字 |
| **数据型** | 科研成果、荣誉奖项、证书资质、专业技能、语言能力 | 每条是短条目（列数据），通常 10–40 字 |

> 教育背景有专用的 `.edu-item` 布局，不参与分栏分类。描述型 section **永远不分栏**，无论测量结果如何。

> 🔒 **分栏是测量后的补救手段，不是初始布局选择。Step 2 生成 HTML 时所有 section 均为单栏，Step 2.5 测量超出 95% 后才按需启用分栏。**

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

**Step 2.5: Browser Overflow Verification & Adaptive Layout (Single-Page Mode Only)**

For `Single-Page Extreme` mode, you MUST verify that the content height fits within the A4 boundary after generating the HTML, and dynamically adjust layout parameters based on the result.

### 2.5.1 Verification Setup

1. Start a local HTTP server (run in background, fire-and-forget):
   `python -m http.server 8766`
   (Run in `OUTPUT_DIR` — the directory containing `index.html`, as a background command)

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
   - **`usage` in 93%–98%** → ✅ Ideal. Proceed to Step 3.
   - **`usage` < 85%** → Too much whitespace. Apply **Expansion Strategy** (see 2.5.3).
   - **`usage` > 100%** → Content overflows. Apply **Degradation Strategy** (see 2.5.2).
   - **`usage` in 85%–93%** → Acceptable but can be improved. Try light expansion.

> ⚠️ **Do NOT wait on HTTP server shutdown!** After verification, proceed immediately to the next step. Leave the HTTP server running in the background. Do NOT call `send_command_input` to terminate it — this causes long blocking delays.

### 2.5.2 Adaptive Layout Degradation Strategy (Overflow → Shrink)

If content **overflows** (usage > 100%), apply the following degradation levels **one at a time**, re-verifying after each adjustment:

| Priority | Action | Description |
|----------|--------|-------------|
| **L1** | Merge education entries into single lines | Combine each education entry (school, major, date) into one line; move secondary info (advisor/direction) inline or omit |
| **L2** | Data-type section column layout | Apply column layout **only to data-type sections** (科研成果、荣誉奖项、证书资质、专业技能、语言能力). Never apply to narrative-type sections. See **L2 Column Layout Procedure** below. |
| **L3** | Reduce padding/margin | Shrink `.a4-page` padding (minimum `10mm 13mm`), section/item margins |
| **L4** | Reduce font size | Freely adjust while maintaining visual hierarchy. Minimum: **9.5pt** |
| **L5** | Prompt the user | If L4 still overflows, stop adjusting and suggest: "Content is too dense for a single-page resume. Consider using the multi-page template." |

> 🔒 **Line-height (≥ 1.5) does NOT participate in degradation. Never reduce it.**

> 🔒 **降级后必须闭环验证**：每次 L3/L4 降级后，必须重新测量 usage。如果 usage 落入 **85%–93%**（空白偏多），则**立即触发 Expansion 回填**（见 2.5.3），将 usage 推回 **93%–98%** 理想区间后才能进入 Step 3 生成 PDF。禁止在 usage < 93% 时直接出 PDF。
>
> **降级-回填闭环流程**：
> ```
> Overflow (>100%) → L1/L2/L3/L4 逐级降级 → 重测
>   ├── 93%–98% → ✅ 直接出 PDF
>   ├── <85%   → Expansion 全量回填 (E1–E4)
>   └── 85%–93% → Expansion 轻度回填 (E1+E2 优先)
>         ├── 仍 <93% → 加 E3/E4 → 重测
>         └── 93%–98% → ✅ 出 PDF
> ```
>
> **注意**：降级和扩展应该**逐级施加、每级后重测**，不要一步到位同时施加 L3+L4，否则容易过度压缩。

#### L2 Column Layout Procedure

**触发条件**：当前 usage > 95%，且 L1（合并教育条目）已执行或无法执行，进入 L2。

**执行流程**：

1. **识别并排序数据型 section**（`<h2>` 内容为：科研成果、荣誉奖项、证书资质、专业技能、语言能力）。描述型 section 跳过，不做任何修改。
   - 统计每个数据型 section 的总字符数（所有 `<li>` 文本长度之和）
   - **按字数从多到少排序**，改变 DOM 中这些 section 的顺序（字数多的在上，字数少的在下）

2. **确定分组策略**（🔒 **最多 3 栏，分栏优先选字数最少的 section 放底部并排**）：
   - 数据型 section 只有 1 个且条目 ≥ 4 → 在其 `.section-content` 上加 `section-2col`
   - 数据型 section 只有 1 个且条目 < 4 → 不做任何分栏，跳过 L2
   - 数据型 section 共 2 个 → 两个字数最少的并排为两栏
   - 数据型 section 共 3 个及以上 → **智能判断两栏还是三栏**：
     - 计算末尾 2 个 section 的字数差（`diff2 = max - min`）
     - 计算末尾 3 个 section 的字数差（`diff3 = max - min`，如果不足 3 个则跳过）
     - 若 `diff2 ≤ diff3`：选末尾 2 个用 `data-sections-row` 两栏并排
     - 若 `diff3 < diff2`：选末尾 3 个用 `data-sections-row-3` 三栏并排
     - 被选中的 section 移到最底部并排，其余保持单栏（已按字数降序排好）

3. **确定栏间距**（按各栏内容字数动态调整 `--col-gap`）：
   - 各栏字数均 ≤ 30 字 → `--col-gap: 12px`（紧凑间距）
   - 各栏字数均 ≤ 60 字 → `--col-gap: 16px`（标准间距）
   - 任一栏字数 > 60 字 → `--col-gap: 20px`（宽松间距）
   - 在包裹容器的 `style` 属性中注入该值：`<div class="data-sections-row" style="--col-gap: 16px">`

4. **用 JavaScript 动态修改 DOM**（在已打开的浏览器页面中执行，修改后立即重新测量）：

```javascript
// 找出所有数据型 section 并统计字数
const DATA_TITLES = ['科研成果', '荣誉奖项', '证书资质', '专业技能', '语言能力',
                     'Publications', 'Honors & Awards', 'Certifications', 'Skills', 'Languages'];
const allSections = Array.from(document.querySelectorAll('.section'));
const dataSections = allSections.filter(sec => {
    const h2 = sec.querySelector('h2');
    return h2 && DATA_TITLES.includes(h2.textContent.trim());
});

// 统计每个数据型 section 的字数
const withCounts = dataSections.map(sec => ({
    el: sec,
    title: sec.querySelector('h2').textContent.trim(),
    chars: Array.from(sec.querySelectorAll('li'))
           .reduce((s, li) => s + li.textContent.trim().length, 0)
}));

// 按字数降序排列（字多的在上，字少的在下）
withCounts.sort((a, b) => b.chars - a.chars);

// 将排序后的 section 按顺序重新插入 DOM（放在最后一个描述型 section 之后）
const parent = withCounts[0].el.parentNode;
const lastNarrative = allSections.filter(s => {
    const h2 = s.querySelector('h2');
    return h2 && !DATA_TITLES.includes(h2.textContent.trim());
}).pop();
const insertRef = lastNarrative ? lastNarrative.nextSibling : null;
withCounts.forEach(item => {
    if (insertRef) parent.insertBefore(item.el, insertRef);
    else parent.appendChild(item.el);
});

if (withCounts.length >= 3) {
    // 智能判断两栏还是三栏：比较末尾 2 个 vs 末尾 3 个的字数差
    const tail2 = withCounts.slice(-2);
    const tail3 = withCounts.slice(-3);
    const diff2 = Math.max(...tail2.map(x => x.chars)) - Math.min(...tail2.map(x => x.chars));
    const diff3 = Math.max(...tail3.map(x => x.chars)) - Math.min(...tail3.map(x => x.chars));

    let group, rowClass;
    if (diff2 <= diff3) {
        group = tail2; rowClass = 'data-sections-row';
    } else {
        group = tail3; rowClass = 'data-sections-row-3';
    }

    // 计算间距
    const maxChars = Math.max(...group.map(x => x.chars));
    const gap = maxChars <= 30 ? '12px' : maxChars <= 60 ? '16px' : '20px';

    // 创建并排容器，放在页面最底部
    const wrapper = document.createElement('div');
    wrapper.className = rowClass;
    wrapper.style.setProperty('--col-gap', gap);
    // 初始等宽分配
    wrapper.style.gridTemplateColumns = group.map(() => '1fr').join(' ');
    parent.appendChild(wrapper);
    group.forEach(item => wrapper.appendChild(item.el));

    // ===== 行高迭代平衡算法 =====
    // 从等宽起步，给更高的栏 +5%，直到等高、差距不再缩小、或触达上限
    if (group.length === 2) {
        let pcts = [50, 50]; // 初始各 50%
        const STEP = 5;      // 每次调整步长
        const MAX = 66.6;    // 单栏最大占比
        const MIN = 33.3;    // 单栏最小占比
        let prevDiff = Infinity;
        for (let i = 0; i < 5; i++) {
            wrapper.style.gridTemplateColumns = pcts.map(p => p + 'fr').join(' ');
            const h0 = group[0].el.offsetHeight;
            const h1 = group[1].el.offsetHeight;
            const curDiff = Math.abs(h0 - h1);
            if (curDiff === 0) break; // 完美等高
            if (curDiff >= prevDiff) {
                // 差距没缩小，回退上一步
                if (h0 > h1) { pcts[0] -= STEP; pcts[1] += STEP; }
                else          { pcts[1] -= STEP; pcts[0] += STEP; }
                break;
            }
            prevDiff = curDiff;
            // 给更高的栏 +5%
            if (h0 > h1) { pcts[0] += STEP; pcts[1] -= STEP; }
            else          { pcts[1] += STEP; pcts[0] -= STEP; }
            // 硬上限截断
            if (pcts[0] > MAX) { pcts[0] = MAX; pcts[1] = 100 - MAX; break; }
            if (pcts[1] > MAX) { pcts[1] = MAX; pcts[0] = 100 - MAX; break; }
            if (pcts[0] < MIN) { pcts[0] = MIN; pcts[1] = 100 - MIN; break; }
            if (pcts[1] < MIN) { pcts[1] = MIN; pcts[0] = 100 - MIN; break; }
        }
        wrapper.style.gridTemplateColumns = pcts.map(p => p + 'fr').join(' ');
    }
    // 三栏场景同理（步长 3%，上限 60%，下限 20%）
    // 这里简化：三栏保持等宽，因为三栏差距一般不大

} else if (withCounts.length === 2) {
    // 正好 2 个，直接两栏并排
    const maxChars = Math.max(...withCounts.map(x => x.chars));
    const gap = maxChars <= 30 ? '12px' : maxChars <= 60 ? '16px' : '20px';
    const wrapper = document.createElement('div');
    wrapper.className = 'data-sections-row';
    wrapper.style.setProperty('--col-gap', gap);

    // 初始等宽
    wrapper.style.gridTemplateColumns = '1fr 1fr';
    parent.appendChild(wrapper);
    withCounts.forEach(item => wrapper.appendChild(item.el));

    // ===== 行高迭代平衡算法（同上） =====
    let pcts = [50, 50];
    const STEP = 5, MAX = 66.6, MIN = 33.3;
    let prevDiff = Infinity;
    for (let i = 0; i < 5; i++) {
        wrapper.style.gridTemplateColumns = pcts.map(p => p + 'fr').join(' ');
        const h0 = withCounts[0].el.offsetHeight;
        const h1 = withCounts[1].el.offsetHeight;
        const curDiff = Math.abs(h0 - h1);
        if (curDiff === 0) break;
        if (curDiff >= prevDiff) {
            if (h0 > h1) { pcts[0] -= STEP; pcts[1] += STEP; }
            else          { pcts[1] -= STEP; pcts[0] += STEP; }
            break;
        }
        prevDiff = curDiff;
        if (h0 > h1) { pcts[0] += STEP; pcts[1] -= STEP; }
        else          { pcts[1] += STEP; pcts[0] -= STEP; }
        if (pcts[0] > MAX) { pcts[0] = MAX; pcts[1] = 100 - MAX; break; }
        if (pcts[1] > MAX) { pcts[1] = MAX; pcts[0] = 100 - MAX; break; }
        if (pcts[0] < MIN) { pcts[0] = MIN; pcts[1] = 100 - MIN; break; }
        if (pcts[1] < MIN) { pcts[1] = MIN; pcts[0] = 100 - MIN; break; }
    }
    wrapper.style.gridTemplateColumns = pcts.map(p => p + 'fr').join(' ');

} else if (withCounts.length === 1) {
    const items = withCounts[0].el.querySelectorAll('.item');
    if (items.length >= 4) {
        withCounts[0].el.querySelector('.section-content').classList.add('section-2col');
    }
}

// 重新测量
const el = document.querySelector('.a4-page');
el.style.overflow = 'visible'; el.style.maxHeight = 'none';
el.style.minHeight = '0'; el.style.height = 'auto';
const usage = (el.scrollHeight / 1123 * 100).toFixed(1);
console.log(JSON.stringify({ afterL2: true, usage: usage + '%',
    sectionOrder: withCounts.map(x => x.title + '(' + x.chars + ')').join(' > ') }));
```

4. 重新测量 usage 后：
   - 若 usage 降至 ≤ 95% → ✅ 分栏生效，**将此时浏览器中的完整 HTML（含新 DOM 结构）写回 `index.html`**，然后进入后续步骤
   - 若 usage 仍 > 95% → 继续 L3（减少 padding/margin）

5. **写回 HTML 的方法**：执行以下 JS 获取当前完整 HTML，然后覆写文件：

```javascript
document.documentElement.outerHTML
```

将输出内容写回 `{OUTPUT_DIR}/index.html`，确保分栏结构持久化，不依赖运行时 JS。

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

The adjustment process is iterative. Expect 2–3 rounds to converge on the ideal 93%–98% usage:

```
Round 1: Measure → Adjust → Re-measure
Round 2: Fine-tune → Re-measure
Round 3: (if needed) Micro-adjust → Final confirmation
```

**Target: 93%–98% usage is the sweet spot.** This leaves a minimal visual margin at the bottom without looking empty.

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
- **Line-Height Floor**: 🔒 Line-height minimum is 1.5. Never reduce it.
- **Font Floor**: Never set body font-size below 9.5pt.
- **Measurement Correctness**: Always remove `min-height`, `max-height`, and `overflow` before measuring real content height. Failure to do so will return a fake gap of 0.
- **Target Fill Rate**: Aim for 90%–95% page usage. Below 85% looks empty; above 98% risks content clipping.
- **Iterative Convergence**: Expect 2–3 measurement rounds. Never assume a single adjustment will be correct. Always re-measure after changes.
- **Multiplicative Caution**: `font-size` and `line-height` have multiplicative effects — a small change applies to every line and compounds quickly. Adjust incrementally (+0.3–0.5pt per round).
