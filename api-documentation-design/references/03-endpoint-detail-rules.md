# Endpoint Detail Rules

Use this reference when writing each endpoint section.

## Endpoint Section Template

- API ID and name:
- Business module, resource, page, or service:
- Served component or component group:
- Backend reuse pattern:
- Purpose and trigger:
- Method and path:
- Auth and permission:
- Request headers:
- Request model family:
- Path/query/body parameters:
- Response envelope/model family:
- Response schema:
- Data/model/source trace:
- Snapshot role/reuse rule:
- Data-version context:
- Backend query binding:
- Endpoint dependency rule:
- Report data-service backend contract:
- Service-layer mapping:
- Backend stack and resource model:
- Transformation rules:
- Filter/sort/page execution stage:
- Global filter SQL `WHERE` rules:
- SQL query-writing strategy:
- Component-internal local filter scope:
- Concurrency/thread/worker model:
- Async/offline job strategy:
- Redis/cache strategy:
- Resource pools:
- Timeout/retry/fallback behavior:
- Rate/concurrency limits:
- Health/readiness and observability:
- Frontend compute policy:
- Success example:
- Empty/no-data example:
- Error examples:
- Performance limits:
- Source mode:
- Compatibility notes:
- Status and pending items:

## Interaction Style

Choose the style before writing the endpoint body:

- Synchronous request/response: document request, response, empty/error examples, and latency expectations.
- Async job: document job creation, job id, status/progress polling, cancellation when allowed, timeout, retry/replay, dead-letter behavior, queue/worker limits, idempotency, retention/expiry, result download or callback, permission checks, and failure states.
- Webhook or callback: document event type, delivery URL, signature/auth, retry policy, idempotency key, ordering, duplicate handling, and dead-letter behavior.
- Streaming or SSE: document connection setup, event schema, heartbeat, reconnect, backpressure, timeout, and terminal events.
- Batch import/export: document file format, encoding, max size, validation errors, partial success, generated artifact retention, and download behavior.

## Backend Reuse Pattern

Classify each production-bound endpoint:

- `metadata`: reusable definitions, dimensions, metrics, fields, filter metadata, or dictionaries.
- `filter-options`: option data with cascade, permission, or source-driven behavior.
- `query`: list, table, chart, KPI, ranking, detail, or analytical query using query context.
- `dashboard/snapshot`: coherent widget group or canonical/shared snapshot data cut.
- `export`: async or bounded export reusing query/list filters.
- `action`: mutation/command with idempotency, permission, audit, and status.
- `health/status`: source freshness, readiness, export/job status, or service health.

Document the reusable backend layer or service family: metadata service, permission service, validator, query planner, repository/source adapter, cache service, formatter, export service, action service, or audit service. If the endpoint needs a custom controller/query/DTO shape, state why the common patterns do not fit.

## Request Parameters

For each parameter, document:

- Name, location, type, required status, default, allowed values, example, and description.
- Validation rule and invalid-param error behavior.
- Filter semantics such as inclusive/exclusive date range, timezone, fuzzy search, multi-select, hierarchy selection, and permission-scoped defaults.
- Filter scope: mark each filter as `global/page-level`, `permission-scope`, `route/drilldown`, or `component-internal`. Global/page-level and permission filters for database-backed endpoints must map to SQL `WHERE` predicates or an equivalent source/provider query. Component-internal filters may operate on the already fetched component dataset when the dataset is bounded by the endpoint contract.
- Database query mapping when the source is database-backed: source column, predicate shape, whether it uses a normal/composite/function/full-text index, type consistency, date/range rewrite, optional-filter generation behavior, and any known non-sargable condition.
- Execution stage: whether each filter, sort, pagination, ranking, Top/Bottom, grouping, aggregation, and count is handled by source query, repository query, upstream provider, precompute/cache, or an explicitly bounded client/service post-process.
- Pagination, sorting, export, drilldown, and search behavior when supported. Collection/list/table endpoints must define pagination unless they are provably bounded by a small fixed enum or single-object lookup.
- Reused request model group when applicable: `QueryContext`, `PageRequest`, `SelectionRequest`, `ExportRequest`, or `ActionRequest`.
- Whether the response is component-ready or only format-ready for the frontend. Component-ready means KPI totals, chart series, table rows, ranks, pagination metadata, and business formula fields are already returned by the API.
- Data-vs-presentation boundary: data APIs return structured facts and metadata by default. Avoid backend-assembled display copy, business conclusion paragraphs, rich text, HTML/Markdown, combined value+unit strings, or style-implied labels unless the endpoint contract documents a server-owned legal/audit/notification/error message or governed explanation.
- For report/BI/dashboard endpoints, document report type, report metadata or fixed-contract source, dimension/metric/filter/sort whitelist source, backend-owned SQL/source expression mapping, parameter guardrails, backend-injected tenant/data/field/export permission behavior, cache key permission safety, result freshness/quality metadata, query/export audit behavior, and slow-report governance expectation.
- For snapshot/latest-period reports, document whether the endpoint accepts, defaults, injects, or returns `snapshotDate`, `latestPeriod`, `loadBatch`, `dataVersion`, report version, or source version. A data-bearing endpoint must identify whether it queries its own source/logical/precompute/cache source or derives from a declared canonical/shared snapshot.
- For every data-bearing endpoint, map data-version fields, business filters, route/drilldown params, pagination/sort params, and backend-injected permission/data-scope values to source predicates, upstream provider params, precompute lookup keys, or Redis/cache key segments.

## Response Schema

For each response field, document:

- Field name, type, required/nullability, description, unit, precision, enum dictionary, example, and compatibility notes.
- Array/object nesting, stable ordering, empty-state shape, and omitted-field behavior.
- Derived fields, aggregation grain, formula, rounding, default fill, and source trace.
- Whether the field is stable, experimental, deprecated, or pending confirmation.

When the endpoint uses or may later use a different source table/view/upstream/fixture, document response compatibility:

- Existing response fields are stable contracts and must not be renamed, removed, moved, retyped, rescaled, re-enumed, re-nullable, re-formulated, or re-grained simply because the source changed.
- Source-field changes are represented by `Data/model/source trace`, `Transformation rules`, SQL aliases, DTO serializers, or response adapter mappings.
- New response fields are additive by default. Use the project naming convention; if none exists, use stable English lowerCamel field codes. Document source, meaning, type, unit, precision, nullability, sensitivity/permission, compatibility status, and whether existing clients may ignore the field.
- Breaking response changes require API version, deprecation/migration notes, downstream consumer impact, and regression scope in `Compatibility notes`.

At response-envelope level, document whether the endpoint uses `Page<T>`, `OptionItem[]`, `KpiCard[]`, `SeriesData`, `TaskStatus`, `ColumnMeta[]`, `Meta`, or a custom envelope. Custom envelopes need a reason so backend serializers and tests do not fragment unnecessarily.

For report/dashboard APIs, document the component-facing view model. Do not leave required component formulas, grouping, ranking, filtering, or chart/table series derivation as implicit frontend work unless the exception is bounded and listed as partial.

For data-bearing APIs, keep presentation composition flexible. Prefer fields such as `value`, `unit`, `precision`, `delta`, `trendDirection`, `thresholdLevel`, `reasonCode`, `messageKey`, and `messageParams` over preassembled sentences. If the backend returns conclusion text because it is governed, model-produced, audit-bound, or legally required, also document the conclusion type, source, variables/evidence fields, status/confidence when applicable, and why frontend composition is not sufficient.

Also document column/result metadata when applicable: field code, display name, type, unit, precision, format, enum label source, sensitivity/masking, sort/filter capability, data freshness time, data delay, data quality status, cache status, query time, and request/trace id.

For snapshot/dashboard aggregate responses, distinguish clearly between:

- component data returned for first-screen rendering, such as KPI summaries, cards, and widget groups;
- shared data-version metadata, such as `snapshotDate`, `latestPeriod`, `loadBatch`, `dataVersion`, report version, or source version.
- reusable canonical snapshot data when the response is intentionally a shared source for other endpoints or components.

Metadata may always align related endpoint requests. Business payload may also be reused when the API document declares it as a canonical/shared snapshot or bounded component-group payload, including consumer list, grain, fields, filters, permission scope, version params, cache key, and invalidation behavior. Other endpoints must not consume an undocumented snapshot response payload as hidden state.

For data-bearing endpoints, response metadata must reconcile with the executed query context. If the response returns `snapshotDate`, `dataVersion`, tenant/org scope, or filter echoes, document whether they came from request params, backend defaults, auth/permission injection, or source metadata.

## Examples

Include compact examples for:

- Successful response with representative data.
- Empty or no-permission-scoped data.
- Invalid parameter.
- Unauthorized or token expired.
- Valid token but no permission.
- Upstream/backend/data-source failure when relevant.

## Performance Notes

Document expected QPS/concurrency, latency targets, default and maximum page size, stable default sort, total-count behavior, cursor/keyset pagination need, export limits, timeout expectations, concurrency/thread/worker model, async/offline job strategy for long-running work, Redis/cache/precompute behavior, resource-pool behavior, timeout/retry/fallback behavior, rate/concurrency limits, large result handling, and any known slow filters or joins.

Do not mark collection/list/table APIs `ready` when pagination is missing, the maximum page size is unknown, or a synchronous endpoint can return export-sized/unbounded results.

Do not mark report/BI/dashboard APIs `ready` when the frontend can send raw SQL, table names, column expressions, arbitrary operators, arbitrary sort strings, unregistered metric formulas, or tenant/data-permission scope. Frontend input must select stable codes; backend metadata/config must own source expressions, permission predicates, guardrails, and result formatting.

Do not mark production-bound endpoints `ready` when the backend reuse pattern, reusable request model, response envelope, or service-layer mapping is missing. A one-off controller/query/DTO shape needs an explicit business or technical reason.

Do not mark endpoints `ready` when the documented or implemented path builds or loads a complete candidate dataset/component payload and then applies global filters, permission scope, sorting, pagination, ranking, Top/Bottom, grouping, aggregation, or count logic afterward. Treat page/API-level full-materialize-then-filter as a performance and correctness blocker except for documented component-internal filters over already fetched component data, tiny static enums, or bounded lookup sets.

Do not mark snapshot/latest-period endpoint groups `ready` when metrics, trends, rankings, tables, drilldowns, or exports depend on an undocumented `/snapshot` payload, frontend call order, or application-memory payload. The correct dependency is either a declared canonical/shared snapshot with matching grain/scope/version or a shared data-version context plus request/defaulted/injected params that filter a shared source/logical/precompute/cache layer.

Do not mark data-bearing endpoints `ready` when the document only echoes version/scope values in response metadata but does not show how those values constrain source-side filtering, upstream provider calls, precompute lookup, or cache keys.

Component-internal local filtering is allowed only when the endpoint has already applied global/page-level SQL `WHERE` filters and the returned component dataset is intentionally complete for that component's local interaction scope. Document the difference so frontend teams do not turn global filters into local filtering.

For database-backed endpoints, also document:

- Whether filtering, sorting, pagination, aggregation, joins, Top/Bottom, and counts are pushed down to SQL/database views/repository queries.
- Selected-column/projection rule, including explicit avoidance of `SELECT *` for list/table/chart APIs.
- Which filters are global SQL `WHERE` predicates and which are component-internal local filters over already fetched component data.
- Which request filters map to direct indexed predicates such as `field = ?`, `field IN (...)`, or `field >= ? AND field < ?`.
- Any avoided or unavoidable non-sargable predicates, especially `FUNCTION(field) = ?`, `DATE(field) = ?`, `YEAR(field) = ?`, `TO_CHAR(field) = ?`, `LOWER(field) = ?`, casts, arithmetic on filtered/joined columns, or leading-wildcard search.
- Rewrite rules, such as `DATE(created_at) = ?` becoming `created_at >= ? AND created_at < ?`, and month filters becoming bounded date/time ranges.
- Optional-filter behavior. Avoid high-volume nullable-OR templates such as `(:param IS NULL OR col = :param)`; document generated predicates and safe parameter binding.
- Join keys/cardinality, including tenant/org/partition/composite keys, one-to-many multiplication risk, aggregation-before-join need, and whether `EXISTS`/`NOT EXISTS` is more appropriate than joins for existence checks.
- Dedup/order/set behavior: whether `DISTINCT`, `ORDER BY`, `UNION`, `UNION ALL`, and stable tie-breakers are required.
- Aggregation/window behavior: `WHERE` before `HAVING` where possible, minimal `GROUP BY` columns, filter-before-window expectations, and Top N limit pushdown.
- Plan evidence expectation for risky P0/high-volume queries: `EXPLAIN` / `EXPLAIN ANALYZE`, scanned rows, access method, join order, sort/temp/materialization, and row-estimate risk.
- Required indexes, composite indexes, generated/normalized columns, full-text indexes, or precompute tables when direct predicates cannot support the requested filter at expected volume.
- Connection-pool owner/config, pool min/max, acquire timeout, idle timeout, validation query/health behavior, and whether pooling is managed by the framework/runtime.
- Redis/cache use when applicable: cache key dimensions, TTL, invalidation trigger, permission/user/tenant safety, warmup, stampede protection, and stale/fallback behavior.
- Redis/cache keys for snapshot/latest-period report endpoints include data-version fields such as `snapshotDate`, `latestPeriod`, `loadBatch`, `dataVersion`, report version, or source version. Endpoint caches may share invalidation triggers, and a declared canonical snapshot cache may be a source of truth; an undocumented endpoint cached response must not become another endpoint's source of truth.
- Redis/cache keys for data-bearing endpoints also include every business filter and backend-injected permission/data-scope value that can change the response.
- When Redis is used, document role and usage pattern: metadata/dictionary cache, permission cache, result/widget cache, canonical snapshot cache, rate limit, distributed lock/singleflight, idempotency key, or job progress. Include key template, value shape/size limit, TTL+jitter, invalidation event, miss behavior, stampede protection, fallback, Redis pool/timeouts, and metrics.
- Do not document production Redis usage that relies on unbounded `KEYS`, broad request-path `SCAN`, infinite TTL for mutable data, locks without TTL/owner token, or cache keys that omit tenant/permission/scope dimensions.

For production-bound or upstream-dependent endpoints, also document:

- Bounded worker/thread/executor or runtime-managed concurrency model, including queue/backpressure/overload behavior.
- Async/offline job contract when long-running work exists: create/status/progress/cancel/result endpoints, queue/worker limit, retry/dead-letter policy, idempotency, result retention/expiry, and sample lifecycle.
- Upstream HTTP/API/client pool owner/config, connect/read/overall timeout, bounded retry with backoff/jitter, circuit-breaker or failure-threshold behavior, and fallback/degraded response shape.
- Rate limit, concurrency limit, request-size limit, async/offline export strategy, and overload status/error body for expensive endpoints.
- Observability metrics: request ID, latency percentiles, error rate, timeout/retry count, cache hit ratio, pool usage, queue length, and slow-query evidence where available.

## Simulation Source Notes

- If backend/API implementation needs mock data, document SQLite as the simulation source with schema/table names, seed-data coverage, indexes, and query responsibility.
- JSON examples are allowed for human-readable success/error samples, contract assertions, or OpenAPI examples, but must not be documented as the API data source for local simulation.
