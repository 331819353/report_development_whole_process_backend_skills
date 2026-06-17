# Request Response Auth Rules

Use this reference to define API inventory-level contracts.

## Request Params

List params by location:

- `path`: resource IDs or required drilldown identifiers.
- `query`: filters, period, org scope, pagination, sorting, keyword search.
- `body`: complex filters, export config, action payload, batch IDs.

Prefer reusable request model groups when possible:

- `QueryContext`: period/date/version fields, business filters, route/drilldown params, backend-defaulted params, and backend-injected permission/data scope.
- `PageRequest`: `pageNo`, `pageSize`, `cursor`, `sortBy`, `sortOrder`.
- `SelectionRequest`: stable metric, dimension, field, and filter codes when the report is configurable.
- `ExportRequest`: same query/filter params as the list/query endpoint plus export format, fields, async options, and idempotency key when needed.
- `ActionRequest`: target ID, action type, payload, idempotency key, permission/audit reason, and duplicate-submission behavior.

Do not invent different parameter names for the same concept across endpoints unless the project already has a standard.

Required filter details:

- Param name.
- Type.
- Required or optional.
- Default value.
- Source filter/control.
- Affected model/API behavior.
- Filter scope: global/page-level, permission-scope, route/drilldown, or component-internal.
- Source field or SQL predicate shape, such as `org_id = ?`, `biz_date >= ? AND biz_date < ?`, or `status IN (...)`.
- Index support: indexed / composite-indexed / function-indexed / full-text / unknown / not indexed.
- SQL query-writing notes for database-backed filters: direct/type-consistent predicate, date/month range rewrite, avoided function/cast/arithmetic, avoided leading-wildcard search, and dynamic optional-filter handling.
- Execution stage: source/provider/repository query, precompute/cache, or explicitly bounded client/service post-process. Use `TBD(GAP-*)` when unknown.
- Gap ID if enum/options/default are unknown.

Required data-version details when a report has snapshot/latest-period semantics:

- Snapshot role: overview-only payload, canonical/shared snapshot dataset, bounded component-group response, local/demo artifact, or `TBD(GAP-*)`.
- Version field name: `snapshotDate`, `latestPeriod`, `loadBatch`, `dataVersion`, source partition, or project-specific equivalent.
- Source of truth: filter-options endpoint, health endpoint, metadata endpoint, source table partition, release/snapshot table, or `TBD(GAP-*)`.
- Consumer/reuse endpoints: snapshot/dashboard aggregate, metrics/trend, ranking, table, drilldown, export, and health.
- Defaulting rule when the client omits the version.
- Param ownership: client-supplied, backend-defaulted, backend-injected from auth/permission, or `TBD(GAP-*)`.
- Query binding: source column/predicate, upstream provider param, precompute lookup key, Redis/cache key segment, or `TBD(GAP-*)`.
- Reuse rule: whether other endpoints/components may derive from the snapshot response/materialized snapshot, and if so the required grain, fields, filters, permission scope, version params, cache key, and invalidation behavior.
- Cache-key dimensions and invalidation trigger.
- Rule that data-bearing endpoints either share the version context through their own query/cache inputs or explicitly reuse a declared canonical snapshot; they must not depend on undocumented response payloads or controller memory.

## Common Params

Use stable names unless the project already defines alternatives:

- `periodType`
- `startDate`
- `endDate`
- `orgId`
- `regionId`
- `productId`
- `customerId`
- `projectId`
- `keyword`
- `pageNo`
- `pageSize`
- `sortBy`
- `sortOrder`
- `snapshotDate`
- `latestPeriod`
- `loadBatch`
- `dataVersion`

## Report Data-Service Backend Contract

For report/BI/dashboard APIs, inventory rows must state:

- Default backend stack when no authoritative project stack overrides it: `Python + Flask + database/upstream connection pools + Redis`.
- Report type: fixed, configurable, self-service, detail, summary, dashboard, export, or snapshot.
- Report metadata or fixed-contract source: report definition, dataset, dimensions, metrics, filters, sort fields, cache policy, timeout, max rows, version/status, or `TBD(GAP-*)`.
- Data-version contract: how `snapshotDate/latestPeriod/loadBatch/dataVersion` is exposed, supplied or defaulted, validated, mapped to source/provider predicates or precompute lookup keys, included in cache keys, and reused by related endpoints without creating endpoint-to-endpoint runtime dependency.
- Frontend input rule: stable codes only. Do not plan APIs where the frontend sends raw SQL, table names, column expressions, arbitrary operators, arbitrary sort strings, unregistered metric formulas, or tenant/data-permission scope.
- Backend-owned mapping: how dimension/metric/filter/sort codes map to source/SQL expressions and safe parameter binding.
- Parameter guardrails: required filters, date range, max dimensions, max metrics, max `IN` values, keyword length, default/max page size, max returned rows, and export rows.
- Permission behavior: menu/report access, row/data scope, field masking/visibility, export permission, tenant isolation, and no-permission response.
- Scope filtering: which tenant/org/user/role/data-scope values the backend injects from auth/permission, and which source/provider predicate or cache key segment they map to.
- Result metadata expectation: columns, units, precision, enum labels, page info, freshness, quality status, cache status, query time, and request/trace id.
- Cache safety: report version, dataset/source version, tenant, permission/user/role scope, filters, sorts, pagination, and locale/unit/format dimensions.
- Endpoint dependency/reuse rule: metrics/trend/table/export endpoints either query their own source/precompute/cache by params or explicitly derive from a declared canonical snapshot. App-memory snapshot state is not an authoritative source unless the scope is explicitly local/demo.
- Export/audit/governance: async export lifecycle when large, query/export/download audit, report version/publish/rollback, and slow-report monitoring when production-bound.
- Gap ID when any required report backend decision is unknown.

## Response Contract At Inventory Level

Do not write full API docs here. State:

- Response model ID/name.
- Envelope shape if known, such as `data`, `list + total`, or `taskId`.
- Reusable response envelope when applicable: `Page<T>`, `OptionItem[]`, `KpiCard[]`, `SeriesData`, `TaskStatus`, `ColumnMeta[]`, or `Meta`.
- Row grain.
- Required field groups.
- Empty state behavior.
- Error behavior only when special.

Prefer reusable envelopes and DTO families so backend serializers, tests, and frontend adapters can be shared. Use a custom response shape only when the business interaction requires it and document why.

## Pagination, Sort, Filter

For list/table APIs:

- State pagination as required unless the result is a confirmed single-object lookup or small fixed enum.
- State `pageNo`/`pageSize` or project-specific pagination names, default page size, maximum page size, out-of-range behavior, and total-count behavior.
- State default sort field and order.
- State allowed sort fields.
- State which filters are server-side.
- State that global/page-level filters for database-backed APIs use SQL `WHERE` predicates or equivalent source/provider predicates. Component-internal filters may be local only when they operate on the already fetched component dataset and are not required for global scope, permission scope, pagination, ranking, aggregation, or counts.
- State that global filters, sorting, pagination, ranking, Top/Bottom, counts, and table slicing are applied before response construction. Page/API-level full-materialize-then-filter behavior is not acceptable for list/table APIs except documented component-internal filters over already fetched component data, tiny static enums, or bounded lookups.
- State whether keyword search is fuzzy, exact, or TBD.
- State whether each database-backed filter can use a direct indexed predicate. Avoid inventory designs that require `FUNCTION(field) = ?` on indexed columns; rewrite date/month filters to range predicates and mark unknown index support with a `GAP-*`.
- State optional-filter behavior. Avoid high-volume designs that require universal nullable-OR predicates such as `(:param IS NULL OR col = :param)`; prefer generated predicates with safe parameter binding.

For charts:

- State whether result ordering is meaningful.
- State whether top N and "others" aggregation exist.
- State whether grouping, aggregation, Top/Bottom, and counts are computed by SQL/database query or by an explicitly bounded non-database source. For database authoritative sources, default to SQL pushdown rather than in-memory calculation. Do not plan a chart API that builds the full component dataset and then filters/ranks/groups it after construction.

For mock-derived backend/API implementation:

- State the planned SQLite fixture database/table(s), seed-data coverage, and indexes.
- Do not use JSON files as the API data source. JSON can remain as response examples or assertion snapshots only.

## Auth And Permission

Auth/permission must include:

- Whether authentication is required.
- User identity source if known.
- Data scope: org, region, product, project, customer, role, or field-level.
- No-permission behavior: empty data, hidden field, 403, or hidden action.
- Sensitive-field behavior: full value, masked value, field hidden, role-limited, or `TBD(GAP-*)`.
- Gap ID when unknown.

## Performance Resilience Cache SLA

For every P0 API, state:

- Backend reuse pattern: metadata, filter-options, query, dashboard/snapshot, export, action, or health/status.
- Reused backend layer or service family when known: metadata service, permission service, query planner, repository/source adapter, cache service, formatter, export service, action service, or audit service.
- Expected data volume or row count range.
- Expected QPS/concurrency and peak traffic assumption.
- Latency target or SLA if known.
- Concurrency/thread/worker model when the endpoint is production-bound or expensive.
- Async/offline job strategy when synchronous work may exceed the latency target, including task ID, status/progress, cancellation when allowed, result download/retention, retry/dead-letter behavior, queue/worker limit, and idempotency.
- Cache, precompute, or real-time expectation.
- Redis/cache expectation when useful for hot or expensive queries, including Redis role, key template/dimensions, TTL, invalidation, stampede protection, permission safety, fallback, and observability.
- Cache keys for related snapshot/latest-period endpoints include the shared data-version context, such as `snapshotDate`, `latestPeriod`, `loadBatch`, `dataVersion`, report version, and source version. Do not use application-memory snapshot state as a cross-endpoint cache dependency in production.
- Cache/precompute keys for data-bearing endpoints also include business filters and backend-injected permission/data scope whenever they change the response.
- Database/upstream/cache connection-pool expectation: existing pool / new pool / externally managed, with max size and timeout assumptions.
- Redis/cache pool expectation when Redis is named: bounded pool, connect/read/write timeouts, retry/backoff, and degraded behavior when Redis is slow or unavailable.
- Timeout, retry/backoff, circuit-breaker, and fallback/degraded behavior if relevant.
- Rate limit, concurrency limit, request-size limit, and overload behavior when needed.
- Export row limit or async threshold when the API can export.
- Health/readiness and observability expectation, such as latency, error rate, cache hit ratio, pool usage, queue length, and slow-query evidence.
- Index or precompute requirement for P0 filters, sorts, joins, and aggregations.
- SQL query-writing strategy for database-backed APIs: selected columns, sargable/type-consistent predicates, complete join keys/cardinality, `EXISTS`/`NOT EXISTS` need, `UNION ALL` vs `UNION`, dedup/order necessity, `WHERE` before `HAVING` when applicable, filter-before-window expectation, and `EXPLAIN` / slow-query evidence for risky queries.
- Pagination/default page size/maximum page size for every list/table API.
- Proof that P0 filters, sorts, pagination, ranking, grouping, and aggregations are source-side or provider-side, not full-materialize-then-filter.
- Gap ID when any required performance decision is unknown.

## Export APIs

State:

- Reused filters from list/table API.
- Export format.
- Sync file stream, async task ID, or download URL.
- Max row limit if known.
- Async threshold, timeout, and retry behavior when known.
- Async lifecycle when applicable: create task, poll status/progress, cancel/retry, download result, expiry/retention, queue/worker limits, and dead-letter behavior.
- Permission behavior.

## Action APIs

State:

- Action payload.
- Idempotency key or duplicate-submission behavior.
- Permission rule.
- Success state.
- Failure state.
- Audit/log requirement.
