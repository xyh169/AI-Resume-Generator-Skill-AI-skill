# Multi-Page With Photo Variant

Read this file **only** when:
- layout = `Multi-Page With Photo`

## Template

Use:
- `resources/template_multipage.css`

## Variant Rules

- **Use the `基本信息` block**:
  - Render a dedicated `基本信息` section near the top.
  - Keep the candidate name in the top `.header`; do not duplicate the name inside `基本信息`.

- **Basic-info section is single-column on the left**:
  - Use `.basic-info-layout` with `.basic-info-grid` on the left.
  - Typical fields include gender, degree, political status, phone, email, location, graduation school, or other concise profile fields.

- **Photo area lives on the right**:
  - If the user provides a photo, place it inside `.photo-box`.
  - If the user wants only a reserved slot, use `.photo-slot`.
  - If the user explicitly wants the `Multi-Page With Photo` variant but has not provided the image yet, using `.photo-slot` is acceptable.

- **Label punctuation**:
  - `基本信息` labels should use a Chinese full-width colon `：`.
  - Prefer handling this through CSS (`.basic-info-label::after`) so the HTML content stays clean and reusable.
