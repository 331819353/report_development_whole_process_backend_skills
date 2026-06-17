# Visual Source Abstraction Standard

Use this standard when screenshots, mockups, images, visual references, or browser captures need to become durable knowledge for downstream agents that may not be multimodal.

## Default Decision

Do not store raw screenshots as the primary skill knowledge source.

Use screenshots as temporary evidence, visual QA artifacts, or exact restoration references. For reusable skills and design standards, extract the useful visual knowledge into text and structured contracts so non-multimodal models can use it.

Keep image files only when one of these is true:

- The image is a runtime asset required by a template or product, such as a logo, background, icon, texture, or illustration.
- The image is an approved visual regression baseline, current screenshot, or diff artifact for a runnable UI.
- The task is exact screenshot restoration and the project needs the source image during the active implementation cycle.
- Audit, compliance, defect evidence, or user instruction requires image retention.
- A retrieval system explicitly uses image embeddings and stores metadata, captions, and lifecycle policy with the image.

If none of these applies, preserve the design value through a textual abstraction and discard or avoid copying the raw image.

## Why Image Vectors Are Not Enough

Image embeddings help retrieval, clustering, duplicate detection, and similarity search. They do not by themselves give a text-only model access to the image content.

For non-multimodal downstream models:

- A raw image path is opaque.
- An embedding vector is opaque unless a retrieval service returns human-readable captions, tags, or extracted fields.
- OCR returns visible text but usually misses hierarchy, spacing, intent, color semantics, and interaction behavior.
- Layout detection can return boxes but still needs semantic labels and design decisions.
- A multimodal model or human reviewer should convert the image into a durable text contract before the image leaves the current evidence loop.

Therefore, the canonical artifact should be the extracted visual contract, not the screenshot or vector.

## Visual Pattern Card

Use this structure for screenshot-derived reusable design knowledge:

```yaml
visualPatternId: short-stable-id
sourceKind: screenshot | mockup | browser-capture | design-reference | runtime-asset
retentionPolicy: text-only | keep-temporary | keep-baseline | keep-runtime-asset | keep-audit-evidence
sourceEvidence:
  imagePath: optional-temporary-path
  capturedAt: optional-date-or-run-id
  authority: user-provided | runtime-capture | generated-sample | project-asset
businessIntent: what decision or workflow this visual supports
componentFamily: kpi-card | ranking-card | chart-card | table-card | conclusion-card | page-shell | other
visualPattern:
  name: stable-pattern-name
  variants: []
layout:
  viewportOrCardSize: width-height-or-range
  gridOrSlots: named regions with width/height budgets
  alignmentRules: scan, center, right-align, fixed columns, etc.
contentHierarchy:
  permanentText: titles, labels, values, units, legends
  hiddenOrTooltipText: long labels, definitions, exact formulas
dataContract:
  requiredFields: []
  formulas: []
  numericFormats: []
  sourceAndFreshness: source/freshness rule
interactionContract:
  controls: []
  hover: []
  click: []
  states: loading | empty | error | no-permission | selected | stale
visualTokens:
  colorSemantics: []
  typography: []
  spacing: []
  radiusShadowBorder: []
whyItWorks: []
antiAiRisks: []
acceptanceChecks: []
```

For Markdown-only standards, keep the same sections as headings instead of YAML.

## Extraction Workflow

1. Classify the image role: temporary reference, exact restoration source, visual regression evidence, runtime asset, or reusable design inspiration.
2. If reusable, extract visible text, component family, business intent, layout slots, dimensions, hierarchy, data semantics, interactions, states, and anti-patterns.
3. Normalize the result into a `VisualPatternCard` or an equivalent reference section.
4. Mark the raw image retention policy. Use `text-only` unless a keep condition applies.
5. For similarity retrieval, store text tags and captions next to vectors. Do not rely on vectors alone.
6. Validate by a non-multimodal dry run: another agent should be able to understand and apply the pattern from text alone.

## Extraction Fields By Use Case

| Use case | Extract first | Keep image? |
| --- | --- | --- |
| Reusable component/style skill | Pattern name, anatomy, slot sizes, data contract, visual hierarchy, anti-AI risks, acceptance checks | Usually no |
| Exact screenshot restoration | Source dimensions, visible text, module order, slot rectangles, colors, spacing, assets, deviations | Temporarily yes |
| Visual regression | URL/state/viewport, baseline/current/diff path, threshold, finding ID, changed region | Yes as baseline/evidence |
| Defect report | Screenshot path, viewport, region, observed issue, expected behavior, severity, retest criteria | Yes as evidence |
| Runtime asset | Asset purpose, path, owner, license/source, replacement policy, responsive behavior | Yes |
| Design inspiration | Human-readable principles, reusable pattern, do/don't rules, data/interaction contract | Usually no |

## Anti-Patterns

- Keeping many screenshots in a skill without captions, tags, or extracted rules.
- Using image paths as references in a standard that will be consumed by text-only models.
- Storing embeddings without captions, metadata, or an image-to-text extraction pipeline.
- Treating OCR text as the full design contract.
- Copying user-provided temporary images into long-lived assets without explicit retention reason.
- Making a visual rule depend on a screenshot that future agents cannot inspect.
- Calling a screenshot-derived design "ready" when no text-only reproduction contract exists.

## Acceptance Checklist

- The artifact states whether the image is temporary evidence, runtime asset, visual baseline, audit evidence, or reusable inspiration.
- Reusable knowledge is represented as text and structured fields, not only raw images.
- Any retained image has a retention reason and lifecycle policy.
- A downstream text-only model can extract the pattern's purpose, layout, sizes, components, data fields, interactions, states, and anti-AI rules.
- Embeddings, if used, are paired with captions/tags/extracted metadata.
- Exact restoration and visual regression cases keep source images only for their active evidence purpose.
