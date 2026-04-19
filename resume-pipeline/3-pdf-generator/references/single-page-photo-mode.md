# Single-Page With Photo Mode Reference

Read this file **only** when the selected layout is `Single-Page With Photo`.

## Scope

This mode is a **top-photo variant** of the old single-page flow. It does **not** replace or modify the old `Single-Page No Photo` branch.

Use:
- `resources/template_1page_photo.css`

Also read and follow:
- `references/single-page-mode.md`

The old single-page reference remains the source of truth for:
- verification setup
- overflow degradation
- expansion strategy
- convergence loop
- parameter tuning ranges
- the old `L2` data-section column procedure

## 2.5.1 Layout Intent

This mode is **not** a persistent dual-column resume body.

The page has:
1. A **top intro area**:
   - left side: name + personal information + education
   - right side: photo slot
2. A **single-column body below**:
   - narrative sections
   - data sections

After the top intro area, the resume returns to the same single-column section flow as the old single-page layout.

## 2.5.2 Required Structure

Use the following shell:

```html
<div class="a4-page">
  <div class="single-page-photo-hero">
    <div class="single-page-photo-intro">
      <div class="header">
        <h1>姓名</h1>
      </div>

      <div class="single-page-photo-basic-info">
        <div class="single-page-photo-basic-line">
          <span class="single-page-photo-basic-label">电话</span>
          <span class="single-page-photo-basic-value">13800000000</span>
        </div>
        <div class="single-page-photo-basic-line">
          <span class="single-page-photo-basic-label">邮箱</span>
          <span class="single-page-photo-basic-value">name@example.com</span>
        </div>
        <div class="single-page-photo-basic-line">
          <span class="single-page-photo-basic-label">城市</span>
          <span class="single-page-photo-basic-value">上海</span>
        </div>
      </div>

      <section class="section">
        <div class="section-title"><h2>教育背景</h2></div>
        <div class="section-content">
          <div class="edu-item">
            <div class="edu-header">
              <div>
                <span class="edu-school">学校</span>
                <span class="edu-major">| 专业</span>
                <span class="edu-detail">| 学位</span>
              </div>
              <span class="item-date">时间</span>
            </div>
          </div>
        </div>
      </section>
    </div>

    <div class="single-page-photo-aside">
      <div class="sidebar-photo">
        <div class="photo-box"><img src="photo.jpg" alt="Profile photo"></div>
      </div>
    </div>
  </div>

  <!-- Then render all remaining sections in the normal single-column order -->
</div>
```

Rules:
1. Name and personal information must be **left aligned**.
2. Personal information should be laid out **horizontally** in the intro area when space allows; wrapping is allowed only if needed.
3. Do **not** place a blue underline or horizontal divider below the name/basic-info block.
4. Education must also live in the **left side of the top intro area** in this mode.
5. Within the top intro row, the entire left intro block should sit **bottom-left aligned** so the education block visually connects to the body below instead of floating from the top.
6. The photo stays on the **right side of the top intro area**.
7. The photo size stays fixed at **25mm x 35mm** (1-inch photo slot).
8. The photo area is part of the top shell only. Do **not** move resume sections into that right-side block.
9. After the hero area, render the remaining sections in the usual single-column order.
10. Do **not** create a sidebar data-section area.
11. Do **not** use the old photo-body two-column experiment from previous iterations of this branch.

## 2.5.3 Personal Information Rendering

Recommended fields:
- phone
- email
- city / current location
- other short facts only if the user explicitly included them

Rules:
- Keep labels in blue and values in regular dark text.
- Keep each field concise.
- Prefer one horizontal line of short fields rather than a vertical stack.
- If the line becomes too long, wrap naturally instead of forcing overflow.
- Do **not** repeat these lines elsewhere in the page.
- Do **not** wrap personal info in a normal `.section` block with a section title.

## 2.5.4 Photo-Mode Adaptive Strategy

`Single-Page With Photo` is its **own branch** and should be reasoned about as its own degradation sequence.

It still reuses the old single-page measurement method, parameter ranges, expansion strategy, and convergence loop from `single-page-mode.md`, but the actual overflow steps for this branch are:

- `L1` -> normalize the **hero education block** into compact one-line entries while preserving all facts
- `L2` -> apply the old **data-type section** column procedure only if the page still overflows after `L1`
- `L3` -> tighten page padding, section spacing, and item spacing while keeping the top photo shell intact
- `L4` -> reduce font size while preserving hierarchy; body font must stay `>= 9.5pt`
- `L5` -> stop and ask the user to switch strategy if overflow still remains

Photo-branch guardrails:
- The top intro area stays intact during adaptation.
- Name, personal information, education, and photo remain in the same top shell.
- Education in the hero area may still be normalized by `L1`, but it should not be kicked back into the normal body flow.
- Do **not** convert the whole page into a persistent two-column body.
- `section-2col`, `data-sections-row`, and `data-sections-row-3` remain allowed only because `L2` may need them.
- If the page already fits on one page, skip `L2` entirely; do **not** split short sections like `证书资质` just to chase denser fill.
- Do **not** shrink the photo to rescue overflow unless the user explicitly asks for that behavior.
- Narrative item headers still follow the normal single-page convention: keep a visible `|` between the project/job title and the role / organization text.

## 2.5.5 Photo-Mode Parameter Notes

Photo-specific structure parameters:

| Parameter | Default | Minimum | Maximum |
|-----------|---------|---------|---------|
| top intro column gap | `12mm` | `8mm` | `14mm` |
| photo size | `25mm x 35mm` | fixed | fixed |

All other adaptive ranges follow `single-page-mode.md`.

## Critical Guardrails

- This is still a **separate branch**, not a mutation of `Single-Page No Photo`.
- Keep the old `template_1page.css` and `single-page-mode.md` untouched.
- The body below the photo intro area is still a single-column resume body.
- Do **not** revive the previous photo-mode sidebar-combination search.
- Do **not** emit broken placeholder glyphs such as `?` for fixed labels like `照片位`.
