# Single-Page Mode Reference

Read this file **only** when the selected layout is `Single-Page Extreme`.

## Table of Contents

- `2.5.1 Verification Setup`
- `2.5.2 Adaptive Layout Degradation Strategy`
- `L2 Column Layout Procedure`
- `2.5.3 Expansion Strategy`
- `2.5.4 Iterative Convergence Loop`
- `2.5.5 Parameter Ranges Summary`
- `2.5.6 Quick-Start Parameter Presets`

## 2.5.1 Verification Setup

1. Start a local HTTP server (run in background, fire-and-forget):
   `python -m http.server 8766`
   (Run in `OUTPUT_DIR` — the directory containing `index.html`, as a background command)

2. Open `http://127.0.0.1:8766/index.html` in the browser

3. **Critical: Correct Measurement Method**

   The `.a4-page` element has `min-height: 297mm` and `overflow: hidden`, which means naive `scrollHeight` vs `clientHeight` comparison will return a fake result. You must temporarily remove these constraints to get the true content height:

   ```javascript
   const el = document.querySelector('.a4-page');
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

   Do not use this broken approach:

   ```javascript
   const scrollH = el.scrollHeight;
   const clientH = el.clientHeight;
   ```

4. Interpret the measurement result:
   - `usage` in `93%–98%` -> ideal, proceed to PDF generation
   - `usage` < `85%` -> apply expansion strategy
   - `usage` > `100%` -> apply degradation strategy
   - `usage` in `85%–93%` -> apply light expansion

> Do not wait on HTTP server shutdown. Leave the background server running and continue the workflow.

## 2.5.2 Adaptive Layout Degradation Strategy (Overflow -> Shrink)

If content overflows (`usage > 100%`), apply the following levels **one at a time**, re-verifying after each adjustment:

| Priority | Action | Description |
|----------|--------|-------------|
| `L1` | Merge education entries into single lines | Reflow each education entry into one line while preserving the same facts; move secondary info inline rather than deleting substantive facts |
| `L2` | Data-type section column layout | Apply columns only to data-type sections (`科研成果`, `荣誉奖项`, `证书资质`, `专业技能`, `语言能力`). Never apply columns to narrative sections |
| `L3` | Reduce padding/margin | Shrink `.a4-page` padding (minimum `10mm 13mm`), section margins, and item spacing |
| `L4` | Reduce font size | Adjust while preserving hierarchy. Minimum body font is `9.5pt` |
| `L5` | Stop and ask the user | If `L4` still overflows, stop and suggest switching to multi-page |

Rules:
- Line-height does **not** participate in degradation. Never reduce it below `1.5`.
- After `L3` or `L4`, always re-measure.
- If degradation pushes usage down into `85%–93%`, immediately backfill with expansion steps until the page returns to `93%–98%`.
- Do not apply `L3 + L4` together in one jump unless repeated measurement has already shown smaller steps are insufficient.

Closed-loop flow:

```text
Overflow (>100%)
  -> L1 / L2 / L3 / L4 progressively
  -> re-measure
     -> 93%–98% => export PDF
     -> <85% => stronger expansion
     -> 85%–93% => light expansion
```

### L2 Column Layout Procedure

Trigger condition:
- Current `usage > 95%`
- `L1` has already been applied or is not enough

Execution flow:

1. Identify all data-type sections (`科研成果`, `荣誉奖项`, `证书资质`, `专业技能`, `语言能力`, and their English ATS equivalents)
2. Count characters in each section's `<li>` items
3. Sort these sections by total character count from high to low
4. Choose a grouping strategy:
   - 1 data section with 4+ items -> apply `section-2col`
   - 1 data section with <4 items -> skip L2
   - 2 data sections -> pair the two smallest into `data-sections-row`
   - 3+ data sections -> compare the tail-2 and tail-3 character spread and choose `data-sections-row` or `data-sections-row-3`
5. Set `--col-gap` based on density:
   - all columns <= 30 chars -> `12px`
   - all columns <= 60 chars -> `16px`
   - otherwise -> `20px`
6. Re-measure after the DOM change
7. If usage drops to `<= 95%`, persist the modified DOM back into `index.html`
8. If usage remains `> 95%`, continue to `L3`

JavaScript reference:

```javascript
const DATA_TITLES = ['科研成果', '荣誉奖项', '证书资质', '专业技能', '语言能力',
                     'Publications', 'Honors & Awards', 'Certifications', 'Skills', 'Languages'];
const allSections = Array.from(document.querySelectorAll('.section'));
const dataSections = allSections.filter(sec => {
    const h2 = sec.querySelector('h2');
    return h2 && DATA_TITLES.includes(h2.textContent.trim());
});

const withCounts = dataSections.map(sec => ({
    el: sec,
    title: sec.querySelector('h2').textContent.trim(),
    chars: Array.from(sec.querySelectorAll('li'))
           .reduce((s, li) => s + li.textContent.trim().length, 0)
}));

withCounts.sort((a, b) => b.chars - a.chars);

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

    const maxChars = Math.max(...group.map(x => x.chars));
    const gap = maxChars <= 30 ? '12px' : maxChars <= 60 ? '16px' : '20px';

    const wrapper = document.createElement('div');
    wrapper.className = rowClass;
    wrapper.style.setProperty('--col-gap', gap);
    wrapper.style.gridTemplateColumns = group.map(() => '1fr').join(' ');
    parent.appendChild(wrapper);
    group.forEach(item => wrapper.appendChild(item.el));

    if (group.length === 2) {
        let pcts = [50, 50];
        const STEP = 5;
        const MAX = 66.6;
        const MIN = 33.3;
        let prevDiff = Infinity;
        for (let i = 0; i < 5; i++) {
            wrapper.style.gridTemplateColumns = pcts.map(p => p + 'fr').join(' ');
            const h0 = group[0].el.offsetHeight;
            const h1 = group[1].el.offsetHeight;
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
    }

} else if (withCounts.length === 2) {
    const maxChars = Math.max(...withCounts.map(x => x.chars));
    const gap = maxChars <= 30 ? '12px' : maxChars <= 60 ? '16px' : '20px';
    const wrapper = document.createElement('div');
    wrapper.className = 'data-sections-row';
    wrapper.style.setProperty('--col-gap', gap);
    wrapper.style.gridTemplateColumns = '1fr 1fr';
    parent.appendChild(wrapper);
    withCounts.forEach(item => wrapper.appendChild(item.el));

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

const el = document.querySelector('.a4-page');
el.style.overflow = 'visible';
el.style.maxHeight = 'none';
el.style.minHeight = '0';
el.style.height = 'auto';
const usage = (el.scrollHeight / 1123 * 100).toFixed(1);
console.log(JSON.stringify({
    afterL2: true,
    usage: usage + '%',
    sectionOrder: withCounts.map(x => x.title + '(' + x.chars + ')').join(' > ')
}));
```

Persist the modified DOM with:

```javascript
document.documentElement.outerHTML
```

## 2.5.3 Expansion Strategy (Excessive Whitespace -> Enlarge)

If content has excessive whitespace (`usage < 85%`), enlarge the layout and re-verify.

| Priority | Action | Description | Typical Impact |
|----------|--------|-------------|----------------|
| `E1` | Increase body font-size | `+0.5–1pt` per round | ~30–60px per step |
| `E2` | Increase line-height | Up to `1.8` maximum | ~40–80px across full page |
| `E3` | Increase padding | Up to `14mm 16mm` | ~30–50px total |
| `E4` | Increase section/item margins | section title and item spacing | ~20–40px total |
| `E5` | Increase title font sizes | h1 up to `22pt`, h2 up to `14pt`, item-title up to `12pt` | ~10–20px total |

Expansion pitfall:
- Font-size and line-height have a multiplicative effect.
- A small change can overshoot dramatically.

Recommended approach:
1. First round: `+0.5pt` body font and line-height to `1.5` if needed
2. Re-measure
3. If still low, do a second smaller round with font and spacing
4. Do not change more than 2 parameters at once

## 2.5.4 Iterative Convergence Loop

Expect 2–3 rounds to converge:

```text
Round 1: Measure -> Adjust -> Re-measure
Round 2: Fine-tune -> Re-measure
Round 3: Micro-adjust -> Final confirmation
```

Target:
- `93%–98%` usage is the sweet spot

## 2.5.5 Parameter Ranges Summary

| Parameter | Default | Minimum | Maximum | Impact |
|-----------|---------|---------|---------|--------|
| body font-size | `9.8pt` | `9.5pt` | `13pt` | High |
| line-height | `1.5` | `1.5` | `1.8` | High |
| `.a4-page` padding | `12mm 15mm` | `10mm 13mm` | `14mm 16mm` | Medium |
| h1 font-size | `16pt` | `14pt` | `22pt` | Low |
| h2 font-size | `12pt` | `11pt` | `14pt` | Low |
| item-title font-size | `10.5pt` | `9.5pt` | `12pt` | Low-Medium |
| `.item` margin-bottom | `4px` | `2px` | `8px` | Low-Medium |
| `.section-title` margin | `5px 0 4px 0` | `3px 0 2px 0` | `8px 0 6px 0` | Low |

## 2.5.6 Quick-Start Parameter Presets

Recommended starting points by content volume:

| Content Volume | body font | line-height | padding | h1 | h2 | item-title |
|---------------|-----------|-------------|---------|----|----|------------|
| Light (3–4 sections, <15 bullets) | `11pt` | `1.6` | `12mm 15mm` | `18pt` | `13pt` | `11pt` |
| Medium (5–6 sections, 15–25 bullets) | `9.8pt` | `1.5` | `10mm 14mm` | `16pt` | `12pt` | `10.5pt` |
| Heavy (6+ sections, 25+ bullets) | `9.5pt` | `1.5` | `10mm 13mm` | `16pt` | `11pt` | `9.5pt` |

These are starting points only. Always verify with real browser measurement and iterate.
