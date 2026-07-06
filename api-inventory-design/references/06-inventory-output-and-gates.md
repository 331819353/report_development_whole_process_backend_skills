# API Inventory Output And Gates

## Hard Constraints

- Each API must trace to a visible page need, interaction, export, dynamic option, or system action.
- Do not turn conflicting artifacts into endpoint assumptions; unresolved `P0`/`P1` authority conflicts keep affected APIs `partial` or `blocked`.
- Each API must trace to one response model and at least one source/logical model unless explicitly pending.
- Existing response model fields must remain stable across mock-to-source, table-to-table, or upstream replacement. The API inventory must not rename, remove, or reshape existing response fields simply because the backend source changed.
- New response fields are additive by default and must follow the project naming convention, or stable English lowerCamel when no convention exists, with source/model trace and compatibility status.
- Filter option APIs are first-class APIs when options are dynamic, permission-limited, cascaded, or source-driven.
- Export APIs must state whether they reuse list filters and whether they return file streams, task IDs, or async download links.
- Mutation/action APIs must define idempotency, permission, success state, failure state, and audit need.
- Do not create "万能接口" that mixes unrelated grains, permission scopes, or refresh cadences.
- Do not create one-off endpoint shapes when a reusable backend pattern fits. A custom route is acceptable only when the inventory states why common metadata/filter/query/export/action patterns do not apply.
- Do not mark table-backed APIs `ready` before table-content evidence exists for every involved table/view/fixture/upstream object: row grain, keys, filter fields, representative rows, permission fields, result bounds, and gaps.
- Do not mark client-visible filters `ready` unless they are request params mapped to source predicates. UI-only selected state, controller defaults, previous endpoint state, or application memory are not filter contracts.
- Do not keep an API inventory shape that is traceable but unreasonable. Use `DESIGN-*` findings for endpoint grouping, grain, filter, permission, export, action, or performance choices that would make downstream implementation or frontend integration awkward or incorrect.
- Do not make one data-bearing API a hidden runtime prerequisite for another. A snapshot/dashboard aggregate API can provide first-screen component data, data-version metadata, and even a canonical shared dataset when the contract says so. Metrics/trends/rankings/tables/drilldowns/exports may reuse that snapshot only when the inventory records the source role, grain, filters, permission scope, data-version params, cache key, and invalidation rule. Shared `snapshotDate/latestPeriod/loadBatch/dataVersion` belongs in request/response/cache context, not in hidden endpoint state.
- Do not mark data-bearing APIs `ready` when data-version, business filters, or permission scope are response-only metadata. They must drive backend params, source/provider predicates, precompute lookup keys, declared snapshot reuse rules, or Redis/cache keys.
- Do not mark an API `ready` when its response model, formula, permission, or source dependency is missing.
- Do not mark a P0 API `ready` when performance/cache/SLA, expected volume, or export limit is unknown and undocumented.
- Do not mark collection/list/table APIs `ready` without pagination, maximum page size, stable sort, and large-result handling.
- Do not mark simple table retrieval APIs `ready` when they require joins, grouping, aggregation, exact counts, ranking, Top/Bottom, formulas, totals, or page/API-level full-materialize-then-filter behavior. The inventory must either query an existing source-aligned table at the needed grain or mark a derived/summary/precompute `GAP-*`. Component-internal filters must be separately scoped to already fetched component data.
- Do not mark filter-bearing APIs `ready` until data completeness is proven before filter binding: option source, source/provider rows, required fields, default/non-default states, empty/no-permission states when relevant, and resolver/API branch behavior are present or linked to `GAP-*`.
- When the inventory feeds default backend/API implementation, assume `Python + Flask + database/upstream connection pools + Redis` and record cache/pool expectations. Use another backend stack only when the user or existing project explicitly overrides it.
- Do not plan JSON files as the simulation data source for backend/API implementation. Use SQLite schema, seed rows, and indexes for mock-derived local APIs.
- Do not leave required table cells blank. Use `none` when intentionally not applicable, or `TBD(GAP-*)` when unknown.


## Required Output

Use a table with these columns:

- API ID.
- Page/module.
- Business purpose.
- Method and path.
- Trigger.
- Request params.
- Response model.
- Source model dependency.
- Response compatibility: preserved existing fields, additive fields, naming convention, and breaking/versioning notes.
- Backend reuse pattern and common request/response model.
- Minimal implementation mode: source-query-simple / derived-summary-exception / blocked, plus table-content evidence link.
- Request-param-to-source-field mapping.
- Snapshot role, data-version context, backend filter params, and endpoint dependency/reuse rule.
- Auth/permission.
- Pagination/sort/filter.
- Filter data support: option source, row grain, default/non-default states, resolver/API branch need.
- Filter/sort/page execution stage.
- Performance/cache/SLA.
- Backend stack/cache/pool expectation and override reason when not using the default backend stack.
- Priority.
- Status.
- Pending questions.
- Design reasonableness status and linked `DESIGN-*` findings when applicable.


## Quick Quality Gate

- All prototype/mock data consumers are represented by an API or documented as static/offline.
- API names and paths are stable enough for downstream API documentation, implementation, or validation.
- Every production-bound API row has a backend reuse pattern or an explicit reason for a custom route/query.
- Every table-backed API row has table-content evidence and a minimal implementation mode.
- Client-visible filters are request params with source predicate mapping.
- API inventory design reasonableness is checked; unresolved `P0`/`P1` `DESIGN-*` findings keep affected APIs `partial` or `blocked`.
- Snapshot/latest-period reports declare the snapshot role and shared data-version context; API rows either declare valid snapshot reuse or avoid hidden dependency on undocumented runtime payload, frontend call order, or controller memory.
- Data-version, business filter, and permission scope values are mapped to backend query params, source-side predicates/precompute lookups, and cache keys for every data-bearing API.
- Request params cover all required filters, drilldowns, pagination, sorting, exports, and actions.
- Filter-bearing APIs prove data completeness before downstream binding; missing non-default data, option rows, fields, or resolver/API branches are visible `GAP-*` items.
- List/table APIs have bounded pagination and documented default/max page size.
- API rows do not depend on hidden aggregation/processing or page/API-level full-materialize-then-filter behavior; source-query-simple boundaries, derived/summary exceptions, and component-internal local filter scope are explicit or linked to a `GAP-*`.
- Response model names match the 数据模型文件.
- Source replacement plans preserve existing response fields and document additive/new field naming before downstream API documentation or backend implementation.
- Missing model/source/formula/enum/permission items are visible instead of hidden in notes.
