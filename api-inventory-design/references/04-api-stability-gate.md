# API Stability Gate

Use this gate before finalizing API清单.

## Required Traceability

Every API row must trace:

- Page/module or interaction.
- Concrete component or component group served by the API.
- Trigger.
- Backend reuse pattern: metadata, filter-options, query, dashboard/snapshot, export, action, or health/status.
- Request params.
- Snapshot role and reuse rule when snapshot/latest-period semantics exist.
- Data-version context when snapshot/latest-period semantics exist.
- Response model.
- Source/logical model dependency.
- Endpoint dependency/reuse rule: whether the API reads source/logical/precompute/cache directly or derives from a declared canonical snapshot.
- Backend query binding: which request/defaulted/injected params constrain source predicates, upstream params, precompute lookup keys, or Redis/cache keys.
- Reused request/response model family, or a documented reason for a custom shape.
- Auth/permission rule.
- Performance/resilience/cache/SLA rule.
- Report data-service backend rule when report/BI/dashboard APIs are in scope.
- Frontend compute policy: component-ready or format-only.
- Priority and status.
- Gap IDs for unresolved items.

## No-Invention Checks

Create a `GAP-*` item instead of inventing:

- Physical source dependency.
- Formula dependency.
- Enum/filter option source.
- Permission rule.
- Response model fields not present in 数据模型文件.
- Component-ready API response shape, when the frontend would otherwise need to calculate metrics, aggregate rows, rank values, split component data, or apply business filters.
- Report data-service backend behavior when report APIs are in scope: report metadata or fixed-contract source, whitelists, backend-owned SQL/source mapping, parameter guardrails, permission injection, result metadata, cache safety, export lifecycle, audit, freshness/quality status, or slow-report governance.
- Performance/resilience/cache/SLA behavior for P0 APIs.
- Redis/cache strategy when a hot or expensive query needs acceleration.
- Backend reuse pattern and common request/response model family. Do not invent a one-off controller/query/DTO shape when a metadata, filter-options, query, dashboard/snapshot, export, action, or health/status pattern fits.
- Database/upstream/cache connection-pool behavior for database-backed or upstream-dependent APIs, including release/close on `ApiError`, timeout, cancellation, early return, and generic exception paths.
- Async/offline job strategy for long-running exports, heavy aggregation, batch import, report generation, or multi-upstream fan-out.
- SQL query-writing strategy for database-backed APIs: projection, predicate shape, join cardinality, dedup/order necessity, pagination/keyset strategy, aggregation/window placement, dynamic optional-filter strategy, or plan-evidence need.
- Expected volume, concurrency model, export limit, timeout, retry/backoff, circuit-breaker, fallback, rate/concurrency limit, or observability behavior when it affects implementation or validation.
- Pagination, maximum page size, stable sort, total-count behavior, or cursor/keyset need for list/table APIs.
- Source/provider/repository execution stage for filters, sorting, pagination, ranking, Top/Bottom, grouping, aggregation, and counts; do not invent this when it is unknown.
- Data-version source and cache-key behavior for snapshot/latest-period reports, including `snapshotDate`, `latestPeriod`, `loadBatch`, `dataVersion`, report version, or source version.
- Source predicate, upstream provider param, precompute lookup key, or Redis/cache key mapping for any data-version, business filter, or permission/data-scope value that changes the result.
- Snapshot reuse role. Do not invent or accept a design where metrics, trends, rankings, tables, drilldowns, or exports depend on an undocumented snapshot/dashboard API response, controller memory, or frontend call order. Declared canonical snapshot reuse is valid when grain, scope, fields, params, cache key, and invalidation are clear.
- SQLite fixture source plan when backend/API implementation needs mock data.
- Action success/failure behavior.

## Path Naming

If no existing convention exists, use:

- Prefix: `/api/reports/{domain}`
- Summary: `/summary`
- Trend: `/trend`
- Ranking: `/ranking`
- Table/list: `/records`
- Detail: `/records/{id}`
- Filter options: `/filter-options`
- Export: `/export`
- Action: `/actions/{actionName}`

Keep paths stable, lowercase, and noun-led. Do not mix Chinese and English path segments.

## Readiness Decision

Mark an API:

- `ready`: backend reuse pattern, response model, source or declared snapshot dependency, request params, reused request/response model family or custom-shape reason, data-version context when applicable, backend query binding, endpoint dependency/reuse rule, permission, report data-service backend behavior when applicable, frontend compute policy, pagination/performance-resilience/cache/SLA, source-side global filter/sort/page execution, component-internal filter scope, SQL query strategy when database-backed, connection-pool behavior including `ApiError` cleanup, async/offline strategy when needed, and priority are clear.
- `partial`: assumptions exist but are linked to gaps and do not block API documentation.
- `blocked`: missing source, model, formula, backend reuse pattern, reused model family or custom-shape reason, snapshot reuse rule when relevant, data-version context for snapshot/latest-period semantics, backend query binding for data-version/business/permission scope, endpoint dependency/reuse rule, permission, report data-service backend behavior when applicable, frontend compute policy, pagination/performance-resilience/cache/SLA, source-side global filter/sort/page execution, component-internal filter scope, SQL query strategy when database-backed, connection-pool behavior, async/offline strategy for long-running work, SQLite fixture source plan for mock-derived implementation, or interaction rule prevents reliable API documentation.

If any P0 API is `blocked`, the overall API清单 is not ready for downstream API documentation, implementation, integration, or validation.

## Blank Cell Rule

Do not leave required API inventory cells blank.

- Use `none` when a column is intentionally not applicable.
- Use `TBD(GAP-*)` when the value is unknown.
- A row with `TBD(GAP-*)` cannot be `ready`.
