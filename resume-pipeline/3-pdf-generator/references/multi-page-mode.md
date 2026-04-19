# Multi-Page Shared Mode Reference

Read this file **only** when the selected layout is `Multi-Page With Photo` or `Multi-Page No Photo`.

## Scope

This file contains the **shared** rules for both multi-page variants:
- `Multi-Page With Photo`
- `Multi-Page No Photo`

Do not mix these rules into the single-page flow.

## Shared Multi-Page Rules

- **Keep the top header name bar**:
  - Retain the top `.header` with the candidate name and underline in all multi-page variants.
  - Do not move the name into another grid or side block.

- **Content can flow across pages naturally**:
  - Multi-page mode does **not** use the single-page measurement, degradation, or expansion loop.
  - Let content paginate naturally according to the browser/PDF engine and the CSS `@page` rules.

- **`page-break-before` remains available**:
  - When a forced new page is necessary, use `.page-break-before`.
  - Do not invent a different break-control class.

- **Blue guide line must be content-aware**:
  - The left blue guide line must follow **actual content blocks**, not the full height of `.section-content`.
  - It should stay continuous across inter-item spacing when more text exists below.
  - It must not extend into the blank tail area at the bottom of a page or below the last real content block.

- **Typography remains layout-driven, not measurement-driven**:
  - You may still inject reasonable font sizes and spacing for readability.
  - Do not run the single-page shrink/expand loop or apply single-page target-usage thresholds.

- **Do not encode user-specific data into the template or skill**:
  - Keep examples generic.
  - Never hardcode a real candidate's name, phone number, email, address, school, or other personally identifying details into the shipped skill or CSS assets.
