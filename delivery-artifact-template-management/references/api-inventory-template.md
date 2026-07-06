# API Inventory Template

Use this exact table for API清单.

## Document Metadata

| Field | Value |
| --- | --- |
| Document version | TBD(GAP-*) |
| Updated at | TBD(GAP-*) |
| Owner | TBD(GAP-*) |
| Decision source | TBD(GAP-*) |
| Overall status | partial |
| Gap IDs | TBD(GAP-*) |

## API Inventory Table

| API ID | Page/module/component | Business purpose | Method and path | Trigger | Request params | Request-param-to-source-field mapping | Response model | Source model dependency | Minimal implementation mode | Table-content evidence | Auth/permission | Pagination/sort/filter | Filter/sort/page execution stage | Report data-service backend | SQL query strategy | Frontend compute policy | Performance/resilience/cache/SLA | Priority | Status | Pending questions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Column Rules

- `API ID`: use `API-001`, `API-002`, or keep existing stable IDs.
- `Page/module/component`: use the page, tab, and concrete data-bearing component or interaction name from requirements/prototype. Prefer one API row per component unless the endpoint splitting rules justify a component group.
- `Business purpose`: write the decision or task this API supports.
- `Method and path`: use stable REST-like paths when no convention exists.
- `Trigger`: use controlled values from the trigger list.
- `Request params`: list path/query/body params at inventory level.
- `Request-param-to-source-field mapping`: map every client-visible filter/sort/page param to source field, operator, default/required behavior, and backend-injected scope; use `TBD(GAP-*)` when unknown.
- `Response model`: use `RSP-*` or response model names from 数据模型文件.
- `Source model dependency`: use `SRC-*`, `LGM-*`, or `TBD(GAP-*)`.
- `Minimal implementation mode`: use `source-query-simple`, `derived-summary-exception`, `non-table-action`, or `blocked`. `source-query-simple` means one source-aligned table/query path with projection, predicates, stable order, pagination, and no hidden aggregation/processing.
- `Table-content evidence`: cite inspected table/view/fixture/upstream object, row grain, keys, filter fields, representative rows, permission fields, result bounds, and `GAP-*`.
- `Auth/permission`: state auth need and data scope, or `TBD(GAP-*)`.
- `Pagination/sort/filter`: state applicable rules or `none`; distinguish global/page-level filters from component-internal local filters.
- `Filter/sort/page execution stage`: for `source-query-simple`, state source/provider/repository execution for global filters, sorting, and pagination, and confirm there is no hidden ranking, grouping, aggregation, Top/Bottom, exact count, formula, total, or broad in-memory processing. Use `TBD(GAP-*)` when unknown. Do not use `ready` when the plan depends on full-materialize-then-filter behavior. Component-internal filters may be `bounded-local` only when they operate on the already fetched component dataset.
- `Report data-service backend`: for report/BI/dashboard APIs, state report type, metadata/fixed-contract source, dimension/metric/filter/sort whitelist source, backend-owned SQL/source mapping, parameter guardrails, permission/tenant/field/export behavior, cache safety, result metadata/freshness/quality, export/audit/governance expectation, or `TBD(GAP-*)`; use `none` when not a report data-service API.
- `SQL query strategy`: for database-backed APIs, state SQL pushdown scope, selected-column/projection rule, index-friendly predicate shapes for filters/sorts such as `org_id = ?` or `biz_date >= ? AND biz_date < ?`, pagination/keyset strategy, dynamic optional-filter strategy, and plan-evidence need. Include join/aggregation/window/count strategy only for `derived-summary-exception`; use `none` when not database-backed.
- `Frontend compute policy`: state `component-ready`, `format-only`, or `TBD(GAP-*)`. Use `component-ready` when the backend/API returns the fields, totals, series, ranking, pagination, and formulas needed by that component. Use `format-only` only when the frontend is limited to display formatting, enum labels, null handling, or trivial unit presentation.
- `Performance/resilience/cache/SLA`: state latency target, expected volume/concurrency, concurrency/thread/worker model, Redis/cache/precompute rule, database/upstream/cache connection-pool behavior, async/offline job threshold for long-running work, export limit, timeout/retry/fallback note, rate/concurrency limit, observability note, or `TBD(GAP-*)`.
- `Priority`: `P0`, `P1`, or `P2`.
- `Status`: `ready`, `partial`, or `blocked`.
- `Pending questions`: list `GAP-*` IDs and one short question.

Required cells must not be blank. Use `none` when intentionally not applicable, or `TBD(GAP-*)` when unknown.

## Controlled Trigger Values

- `initial-load`
- `filter-change`
- `drilldown`
- `export`
- `action`
- `scheduled`

## Priority Rules

- `P0`: needed for first usable page, first-screen conclusion, required dynamic filters, required detail, or required permission behavior.
- `P1`: important drilldown, secondary chart/table, normal export, or advanced filter.
- `P2`: enhancement, optional export, non-core action, or future expansion.

## Status Rules

- `ready`: request params, request-param-to-source-field mapping, response model, source dependency, minimal implementation mode, table-content evidence, permission, filter/sort/page execution stage, report data-service backend behavior when applicable, SQL query strategy when database-backed, frontend compute policy, performance/resilience/cache/SLA, and priority are clear.
- `partial`: safe assumptions exist and are linked to gap IDs.
- `blocked`: source, formula, permission, grain, table-content evidence, request-param mapping, response model, filter/sort/page execution stage, report data-service backend behavior when applicable, SQL query feasibility, frontend compute policy, performance/resilience/cache/SLA, or required interaction is unknown.
