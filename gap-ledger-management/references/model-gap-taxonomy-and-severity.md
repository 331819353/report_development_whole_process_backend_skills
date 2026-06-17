# Gap Taxonomy And Severity

Use this reference to classify pending model items consistently.

## Categories

Use exactly one primary category per row:

- `source-system`
- `requirement-scope`
- `page-module`
- `interaction`
- `acceptance-criteria`
- `prototype-code`
- `table-view-file-api`
- `field-metadata`
- `join-key`
- `metric-formula`
- `enum-dictionary`
- `dimension-hierarchy`
- `sample-data`
- `permission`
- `data-security`
- `refresh-cadence`
- `data-quality`
- `response-model`
- `prototype-mapping`
- `ownership`
- `performance`
- `other`

## Owner Values

Use the most likely owner:

- `business`
- `data-owner`
- `backend`
- `frontend`
- `sso-security`
- `platform`
- `testing`
- `product-owner`
- `unclear`

## Severity Rules

- `Blocker`: prevents reliable API清单, 数据模型文件, API documentation, implementation handoff, integration, or validation.
- `High`: allows documentation but risks wrong data, formula, permission, source traceability, or user-facing result.
- `Medium`: affects edge cases, examples, secondary filters, or non-core details.
- `Low`: naming, copy, metadata polish, or non-blocking clarification.

Severity cannot be `Low` when the gap affects:

- Core metric formula.
- Source table/view/API identity.
- Join key.
- Permission rule.
- Sensitive field masking or field-level permission.
- Response model field required by a P0 API.
- Refresh cadence for time-sensitive data.
- Performance/cache/SLA expectation for a P0 API.
- Required page, interaction, or acceptance criterion.

## Impact Phrases

Use clear impact phrases:

- Blocks API清单.
- Blocks 数据模型文件.
- Blocks API文档.
- Blocks backend implementation.
- Blocks frontend binding.
- Blocks testing/acceptance.
- Blocks page/API scope decision.
- Blocks interaction contract.
- Blocks performance/SLA decision.
- Risks wrong metric result.
- Risks permission leakage.
- Risks sensitive data exposure.
- Risks inconsistent filter behavior.
- Needs business confirmation only.
