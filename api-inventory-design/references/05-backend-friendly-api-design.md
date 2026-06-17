# Backend-Friendly API Design

Use this reference when an API inventory or API document should make backend implementation simple, efficient, and reusable.

Backend-friendly does not mean fewer endpoints at any cost. It means endpoint boundaries, request models, response models, and lifecycle patterns can flow through reusable backend layers instead of creating one custom controller and one custom query for every page widget.

## Core Principle

Every data-bearing API should declare its backend reuse pattern:

- `metadata`: report/page/query definitions, dimensions, metrics, fields, enum dictionaries, display metadata.
- `filter-options`: dynamic, cascaded, permission-scoped, or source-driven option lists.
- `query`: list, table, chart, KPI, ranking, detail, or analytical query using a shared query context.
- `dashboard/snapshot`: coherent widget group or canonical/shared data cut.
- `export`: async or bounded export that reuses the query/list filter contract.
- `action`: mutation or operational command with idempotency, permission, audit, and status.
- `health/status`: data freshness, source readiness, job status, export status, or service health.

An API row without a reuse pattern is harder for backend teams to implement consistently.

## Reusable Backend Pipeline

Design APIs so backend code can reuse this pipeline:

```text
Controller
-> Auth/Permission
-> Request Validator
-> Query Context Builder
-> Metadata / Whitelist Lookup
-> Query Planner
-> Repository / Source / Precompute / Cache
-> Result Formatter
-> Audit / Observability
```

The API contract should provide enough information for each layer:

- stable route and method;
- stable request model;
- backend-defaulted and backend-injected params;
- field/metric/filter/sort codes instead of raw SQL or arbitrary expressions;
- reusable response model;
- cache/precompute and pagination/export behavior;
- error, empty, no-permission, timeout, and degraded states.

## Request Model Rules

Prefer reusable request shapes:

- `QueryContext`: tenant/user/role/data scope, data version, time range, org/product/customer/project filters, keyword, drilldown params.
- `PageRequest`: `pageNo`, `pageSize`, `cursor`, `sortBy`, `sortOrder`.
- `MetricSelection`: metric codes and dimension codes when configurable.
- `ExportRequest`: same query/filter request as the list/table/query API plus export fields, format, and async options.
- `ActionRequest`: target ID, action type, payload, idempotency key, and reason/comment when needed.

Do not design endpoint-specific parameter names for the same concept unless the project already has a standard. Reusing parameter names lets backend validators, query builders, cache-key builders, and tests be shared.

## Response Model Rules

Prefer reusable response envelopes and typed payloads:

- `Page<T>`: rows, page/cursor, total strategy, hasNext.
- `OptionItem`: code, label, parentCode, disabled, permission/no-data reason when needed.
- `ColumnMeta`: code, label, type, unit, precision, enum, sortable, filterable, sensitivity.
- `KpiCard`: code, label, value, unit, precision, trend, target, status.
- `SeriesData`: x/y/category/series fields, unit, precision, ordering.
- `TaskStatus`: taskId, status, progress, createdAt, finishedAt, resultUrl, error.
- `Meta`: dataVersion, freshness, quality, fromCache, queryTime, requestId.

Do not invent a different envelope per endpoint unless the interaction genuinely requires it. Reusable envelopes reduce serializers, tests, and frontend adapters.

## Endpoint Boundary Rules For Reuse

Merge endpoints only when backend reuse improves and correctness stays clear:

- same query context, permission scope, grain, source dependency, refresh cadence, and cache policy;
- response is a coherent component group or declared snapshot;
- payload remains bounded;
- backend can build it with one query plan, one cache/precompute key family, or one formatter family.

Split endpoints when backend reuse would be harmed:

- different grain or permission scope;
- one endpoint is paginated and another is aggregate;
- one is realtime and another is daily snapshot;
- one requires async export or heavy query grading;
- one needs a different source, cache invalidation, or SLA.

Avoid both extremes: a broad page-level API that forces frontend splitting, and dozens of tiny custom endpoints that each require a one-off controller/query.

## Metadata-Driven Report APIs

For configurable or repeated report patterns, prefer metadata-driven APIs:

```http
GET  /api/reports/{reportId}/metadata
GET  /api/reports/{reportId}/filters
POST /api/reports/{reportId}/query
POST /api/reports/{reportId}/exports
GET  /api/report-exports/{taskId}
```

Frontend requests select stable dimension, metric, filter, sort, and export codes. Backend metadata maps codes to SQL/source expressions, permission predicates, cache rules, and display metadata.

Fixed endpoints are still acceptable for simple fixed reports, but the API inventory should state why metadata-driven reuse is not needed.

## Filter And Export Reuse

- Filter option endpoints are reusable assets. Do not hide dynamic options in unrelated business responses.
- Export APIs should reuse the corresponding list/query request model and permission rule. Do not create a separate export parameter vocabulary unless export has extra fields or async behavior.
- Detail/drilldown APIs should reuse route/drilldown params and parent query context so permission, cache, and test cases are shared.

## Backend Reuse Checklist

Every production-bound API row should answer:

- Which backend reuse pattern does this endpoint use?
- Which common request model does it reuse?
- Which common response model/envelope does it reuse?
- Which query context, metadata, permission, cache, pagination, export, or action service can handle it?
- Which fields/metrics/filters/sorts are stable codes owned by backend metadata?
- Which parts are intentionally custom, and why?

If the answer is "new custom controller and custom SQL for this one widget", record a `DESIGN-*` finding unless the endpoint is truly one-off and low risk.

## Anti-Patterns

- One controller per widget with duplicated permission, filter, metric, cache, and formatter logic.
- API paths named after visual positions rather than stable resource/report/component concepts.
- Same filter meaning with different parameter names across endpoints.
- Each list/table endpoint has a different pagination envelope.
- Export API does not reuse the list/query filters.
- Frontend sends raw SQL, arbitrary column expressions, arbitrary sort strings, or permission scope.
- API response includes business formulas that cannot trace to a reusable metric definition.
- Endpoint split/merge decisions are made only to reduce HTTP request count, not backend query or contract reuse.
