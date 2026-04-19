# Multi-Page No Photo Variant

Read this file **only** when:
- layout = `Multi-Page No Photo`

## Template

Use:
- `resources/template_multipage-2.css`

## Variant Rules

- **Do not render any photo container**:
  - Omit `.photo-box` and `.photo-slot`.
  - Do not reserve a right-side blank area for a future image.

- **Do not emit the photo-layout basic-info block by default**:
  - Omit `.basic-info-layout`, `.basic-info-grid`, and related photo-oriented DOM.
  - Keep personal metadata compact in the top header line by default, similar to the single-page structure.

- **No-photo multi-page is structurally closer to the single-page layout**:
  - Use the standard `.header -> .section -> .section-content -> .item` hierarchy.
  - Preserve multi-page pagination behavior and the shared content-aware guide-line rules from `multi-page-mode.md`.

- **Only add extra profile information when it helps readability**:
  - If the user has many profile fields, render them as normal content blocks using existing section/item DOM.
  - Do not recreate the with-photo grid layout in the no-photo variant.
