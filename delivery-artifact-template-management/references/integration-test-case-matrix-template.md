# Test Case Matrix Template

Use this template when integration test cases need to be handed off as a runnable matrix.

## Coverage Matrix

| Feature/Page | Related API | Control semantics | Filters | Interactions | Permission | State Coverage | Case IDs |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Test Case Columns

| Case ID | Category | Priority | Feature/Page | Related API | Preconditions | Steps | Test Data/Params | Control semantics | Data completeness before filter binding | Height budget / DOM overflow check | Expected Frontend Result | Expected Backend/API Result | Evidence | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Required Categories

- Runtime URL smoke and environment alignment.
- SSO/auth: first access, valid token, invalid token, no permission, logout when supported.
- API/display consistency for KPI cards, charts, tables, drawers, and exports.
- Filter data completeness: option rows, business/API rows, required fields, default state, non-default state, empty/no-permission state, and resolver/API branches.
- Control semantics: perspective-switch vs global-filter vs local-filter vs drilldown-param classification, with schema-changing perspectives separated from ordinary filters.
- Filter behavior: default, single change, combined filters, reset, cascade, no-result, permission-limited option.
- Non-default perspective behavior: every domain/theme/management-object/subject-area view updates metric names, titles/summaries, table dimensions/headers, component set, specialty metrics, risk focus, and口径 labels as specified.
- Cross-perspective consistency: every domain/statistical口径 validates navigation percentages, overview KPIs, journey cards, and chart summaries against one data chain, with at least one field-level equality assertion.
- Fixed-height navigation/card/KPI fit: padding, explicit line-height, gaps, badge/status/footer heights, `requiredContentHeight <= componentHeight`, and DOM checks where `scrollHeight <= clientHeight` and `scrollWidth <= clientWidth` at `1920x1080` and `1280x768`.
- Backend connection-pool resilience: repeated `ApiError`/timeout/exception after connection acquire releases/closes the connection, later requests can still acquire from the pool, and pool max such as `STARROCKS_POOL_MAX` is recorded.
- Interaction behavior: drilldown, drawer, modal, page jump, pagination, sorting, refresh, export/download.
- Edge states: loading, empty, error, timeout, null, partial data, missing optional fields.
- Defect retest: blocker/high/major defects after a fix, with original defect ID, fix version, retest environment, and closure criteria.
- Production acceptance: runtime environment, version alignment, auth mode, source mode, critical data paths, and known-risk regression points.

## Readiness Rules

- Mark a case `blocked` when URL, account, data seed, permission, API document, or acceptance rule is missing.
- Do not remove blocked cases from the matrix.
- Each executable case needs expected frontend behavior, expected backend/API behavior, evidence to capture, and pass/fail criteria.
- Filter behavior cases are executable only after their data-completeness cases pass or are explicitly blocked as data gaps.
- Perspective-switch cases cannot pass on numeric changes alone; schema/wording checks must be captured when `componentSchemaImpact` is not `row-scope-only`.
- Cross-perspective consistency cases cannot pass without source/field evidence for the navigation indicator and at least one equality assertion against overview/journey/chart data.
- Fixed-height navigation/card/KPI fit cases cannot pass on screenshots alone; a DOM result with `scrollHeight > clientHeight` or `scrollWidth > clientWidth` is clipping unless the region is an intentional visible scroll area.
- Do not mark production acceptance `pass` when required retest cases are still `open`, `fixed` without retest, or `blocked`.
