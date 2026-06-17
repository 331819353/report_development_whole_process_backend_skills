# Report Data Service Backend Implementation And Optimization

Use this shared reference whenever a report, BI, dashboard, or data-visualization backend/data service is designed, documented, implemented, validated, or reviewed for production readiness.

This reference is about the report backend as a controlled query service. It complements:

- `$performance-optimization` for OLAP business process, grain, fact/dimension, metric, serving-model design, SQL query shape, execution-plan risk, concurrency, Redis/cache/precompute, pools, async work, timeout, limits, and observability.
- `$redis-cache-design-patterns` for Redis key design, TTL, invalidation, stampede protection, permission safety, fallback, and observability when Redis is named.

## Core Principle

A report backend is not a CRUD wrapper and not a thin SQL proxy. It must control the full query chain:

```text
report definition
-> permission check
-> parameter validation
-> metric and dimension governance
-> query planning
-> safe SQL/source query generation
-> execution
-> cache/precompute
-> result formatting
-> pagination/export
-> audit and monitoring
-> slow-report governance
```

Frontends choose report, dimension, metric, filter, sort, page, drilldown, and export options by stable codes. Frontends must not send raw SQL, table names, column expressions, arbitrary operators, or permission scope.

API design should let this query-service chain be reused. A backend-friendly API declares the reuse pattern, common request model, common response envelope, and service-layer mapping before implementation starts.

## Upstream Technical-Solution Linkage

When a technical solution exists, the data-service design must consume and preserve its decisions:

- `ARC-*`: service boundary, logical architecture, data flow, runtime/deployment, security, and operations views.
- `ADR-*`: selected backend/data-service stack, cache/precompute choice, deployment/runtime, auth/security, observability, and testing/release decisions.
- `API-*`: endpoint families, consumers, request/response model names, performance expectations, and status.
- `SRC-*`, `LGM-*`, `RSP-*`, `MET-*`: source authority, logical model, response model, metric口径, grain, fields, lineage, and data-version fields.
- `PERM-*`, `DQ-*`, `NFR-*`: permission, data quality, performance/resilience, security, observability, and production-readiness constraints.
- `GAP-*`, `RISK-*`, `ROAD-*`: unresolved decisions, risks, owner actions, and implementation phase order.

If upstream artifacts do not exist, produce equivalent decisions in the data-service design and mark uncertain items with linked gaps. Do not infer production runtime, source authority, metric口径, permission scope, or cache behavior without evidence.

## Data-Service Design Contract

Before API documentation or implementation, a production-bound report data service should have a design contract that covers:

| Design Area | Required Output |
| --- | --- |
| Service boundary | owned APIs, consumers, upstream/downstream systems, source authority, out-of-scope work |
| Layered architecture | controller, service/use-case, metadata, query planner, source adapter, formatter, cache/precompute, export, permission, operations |
| Query context | client params, backend defaults, data-version params, backend-injected permission/data scope, guardrails, downstream predicate/key mapping |
| API family mapping | metadata, filter, query, dashboard/snapshot, detail/drilldown, export, action, status/health families and shared models |
| Source adapter mapping | source fields/formulas to response fields, units, precision, enum, null/default behavior, compatibility status |
| Data vs presentation boundary | structured data, units, enums, reason codes, message keys/params, metadata, and documented server-owned text exceptions |
| Runtime model | sync/async boundary, connection pools, Redis/cache/precompute, timeout/fallback, rate/concurrency limits, queue/backpressure |
| Security and audit | auth, tenant/org/data scope, field/action/export permission, masking, secret/config, query/export/download/config audit |
| Production operations | health/readiness, logs, traces, metrics, slow-report governance, freshness/quality signals, alert owner, deployment/rollback |
| Handoff readiness | API documentation, implementation, frontend integration, testing, operations, gaps, risks, owner actions |

Use `data-service-design-template.md` when the deliverable is design rather than implementation.

## Default Backend Stack

For default report backend/data-service planning or implementation, use `Python + Flask + SQLAlchemy + database/upstream connection pools + Redis` unless the user specifies another stack or an existing project has an authoritative backend stack. When SSO and multiple databases are part of the backend, also apply `$python-flask-sso-multidatabase-backend`.

- Flask owns HTTP routing, request validation handoff, service composition, error envelopes, health/readiness endpoints, and auth middleware integration.
- SQLAlchemy owns engine/session management, DBAPI dialect integration, parameter-bound SQL/ORM execution, and a stable abstraction over SQLite/MySQL/Oracle/StarRocks access.
- Database/upstream connection pools own bounded resource usage, acquire timeout, idle/validation behavior, overload protection, and guaranteed release/close on success and exception paths.
- Repository/source adapters must pair every pool acquire with `finally`, context-manager cleanup, `defer`, `using`, or an equivalent guard. `ApiError`, timeout, cancellation, validation error after acquire, formatter error, early return, and generic exception paths must return the connection to the pool or close it before the error envelope is produced.
- For StarRocks-backed services, record the max pool config such as `STARROCKS_POOL_MAX`. A default max such as `STARROCKS_POOL_MAX=5` means a handful of leaked `ApiError` paths can exhaust the pool and block later requests.
- Redis owns cache/precompute, hot query acceleration, dictionary/permission cache where safe, canonical snapshot cache when declared, stampede protection, stale fallback, rate/concurrency support, idempotency keys, distributed locks, and short-lived job progress when needed.
- Document an override reason before choosing FastAPI, Spring, Express, Node, or another backend stack by default.

## Python Flask SSO And Multi-Database Baseline

When the backend project is a Python/Flask service with enterprise SSO and multiple databases, load `$python-flask-sso-multidatabase-backend` and include these decisions in the handoff:

- app factory, config profiles, versioned Blueprints, middleware, service, repository, model, db, schema, utils, SQL, test, WSGI, Docker, and deployment file ownership;
- `Access-Token` header contract and optional `Application-Key` behavior when Haier IAMA/clientId is active;
- backend token validation path, local user mapping, role/permission loading, and strict 401 vs 403 behavior;
- database role map: SQLite local/test, MySQL business/user/permission/config, Oracle enterprise legacy/core source, StarRocks analytics/report/metric query;
- SQLAlchemy engine/session registry, per-database pool config, context-manager or `try/finally` connection release, and dialect-specific SQL directories;
- dependency baseline: Flask, Flask-SQLAlchemy/SQLAlchemy, Flask-Migrate, PyMySQL, oracledb, requests, python-dotenv, redis when used, pytest, gunicorn;
- deployment/runtime baseline: `wsgi.py`, Gunicorn config, Nginx/gateway contract, Docker, env profiles, health/readiness endpoint, and structured logging.

Do not collapse the SSO check, permission logic, SQL query, result mapping, and response formatting into one Flask route handler.

## Required Backend Responsibilities

For each production-bound or production-like report data service, document or implement these responsibilities.

| Area | Required Decisions |
| --- | --- |
| Report metadata | Report definition, report type, dataset, dimensions, metrics, filters, sort fields, display/format metadata, cache policy, timeout, max rows, status, version, owner. |
| Dataset contract | Table/view/API/file source, source authority, source owner, grain, freshness, quality status, source version, data-source type, SQL dialect, and source-specific limits. |
| Query API | Query endpoint, metadata endpoint, filter-option endpoint, dashboard/widget endpoint when needed, async export endpoints, subscription/snapshot/admin endpoints when in scope. |
| Query planner | Selected dimensions/metrics, filter tree, permission predicates, tenant predicates, pagination, sorting, Top N, aggregation, count strategy, query grade, and sync/async decision. |
| SQL/source query builder | Field/metric/operator/sort whitelist, parameter binding, SQL dialect adaptation, tenant/permission injection, generated optional predicates, and safe aliases. |
| Permission model | Menu/report access, row-level data scope, field visibility/masking, export permission, tenant isolation, and no-permission response behavior. |
| Parameter guardrails | Required filters, date-range limits, max dimensions, max metrics, max `IN` values, keyword length, default/max page size, max page depth, max export rows, and invalid-param errors. |
| Cache/precompute | Metadata cache, permission/dictionary cache, result cache, dashboard/widget cache, export-file cache, warmup, invalidation, versioned keys, permission/tenant/user safety, stale fallback. |
| Pagination/count | Bounded pages, stable sort, cursor/keyset need, `hasNext` vs exact total, total-count cost, and deep-page/export handoff. |
| Export | Separate async export lifecycle, batch/stream write, file retention/expiry, row/field permission recheck, watermark/approval when sensitive, audit, and isolated worker pool. |
| Result contract | Component-ready payload, column metadata, units, precision, enum labels, empty/no-permission shape, data freshness, data quality warnings, query time, cache status, and trace/request id. |
| Security and compliance | Sensitive-field masking, secret/config handling, datasource credential encryption, audit logs, download logs, report config change logs, and permission change logs. |
| Stability and governance | Query timeout, rate/concurrency limits, query grading, slow-report monitoring, hot-report/cache-hit monitoring, source isolation, downgrade behavior, release/publish/rollback/offline flow. |

## Recommended Query-Service Layers

Keep controllers thin. A maintainable report backend normally separates these responsibilities:

```text
ReportController
ReportService
ReportMetadataService
ReportPermissionService
ReportParamValidator
ReportQueryPlanner
ReportSqlBuilder / SourceQueryBuilder
ReportQueryExecutor
ReportCacheService
ReportResultFormatter
ReportExportService
ReportAuditService
ReportMonitorService
```

Implementation packages may differ, but controller-level SQL concatenation, permission checks, cache key construction, export logic, and result formatting should not be mixed into one handler.

## Backend-Friendly API Families

Prefer stable endpoint families that map to reusable backend services:

| API Family | Typical Endpoint | Reused Backend Layers |
| --- | --- | --- |
| Metadata | `GET /api/reports/{reportId}/metadata` | metadata service, permission service, dictionary cache, response metadata formatter |
| Filter options | `GET /api/reports/{reportId}/filters` | metadata service, permission service, option repository, cascade resolver, cache service |
| Query | `POST /api/reports/{reportId}/query` | validator, query context builder, query planner, SQL/source builder, executor, cache, formatter |
| Dashboard/snapshot | `GET /api/dashboards/{dashboardId}` or `GET /api/reports/{reportId}/snapshot` | query planner, widget cache, canonical snapshot/precompute, formatter |
| Detail/drilldown | `GET /api/reports/{reportId}/records/{id}` or query drilldown | permission service, query context, repository, formatter |
| Export | `POST /api/reports/{reportId}/exports` | query validator, export service, worker queue, file store, audit |
| Action | `POST /api/reports/{reportId}/actions/{actionName}` | action service, idempotency, permission, audit |
| Status | `GET /api/report-exports/{taskId}` or health endpoint | task store, source freshness, readiness, observability |

API inventories and API documents should identify the family for each endpoint. A custom endpoint family is acceptable only when the common families cannot express the interaction cleanly.

## Reusable Request And Response Models

Use shared request concepts where possible:

- `QueryContext`: data version, time range, business filters, route/drilldown params, backend-injected permission scope.
- `PageRequest`: page/cursor, size, sort field, sort order.
- `SelectionRequest`: stable dimension, metric, field, filter, and sort codes.
- `ExportRequest`: the same query/filter request plus export format, fields, and async options.
- `ActionRequest`: target, action, payload, idempotency key, and audit reason.

Use shared response envelopes where possible:

- `Page<T>` for lists and tables.
- `OptionItem[]` for filters.
- `ColumnMeta[]` for table/chart metadata.
- `KpiCard[]` and `SeriesData` for visual data.
- `TaskStatus` for async work.
- `Meta` for freshness, quality, cache status, query time, and request ID.

Avoid inventing a different parameter vocabulary, response envelope, or error shape for every widget. Reuse reduces validators, DTOs, serializers, tests, and frontend adapters.

## Source Replacement And API Field Compatibility

When a report backend changes from mock/SQLite to real data, or replaces a table, view, upstream API, fixture schema, precompute table, or serving model, treat the existing API response model as the downstream compatibility contract.

Required compatibility work:

- Preserve existing response field names, casing, nesting, types, units, precision, enum meanings, nullability, formulas, grain, sort/export meaning, empty/no-permission behavior, and display semantics.
- Put source-field/table changes inside repository mapping, SQL aliases, DTO serializers, or response adapters. Do not expose raw new table or upstream column names by renaming existing API fields.
- Produce a compatibility matrix: endpoint/model, existing response field, old source field/formula, new source field/formula, transform/default/null rule, verification sample/test, and status.
- Add new response fields only as additive fields. Follow the project naming convention; if none exists, use stable English lowerCamel field codes. Document source, business meaning, type, unit, precision, nullability, permission/sensitivity, and compatibility status.
- Treat unavoidable renames, removals, type/unit/precision/enum/nullability/formula/grain changes, or empty/no-permission behavior changes as breaking. They require API versioning, deprecation/migration notes, downstream frontend/test impact, and rollback/compatibility plan before implementation is accepted.

Good implementation patterns:

- Use explicit SQL aliases or serializer mapping such as `new_table.completed_pct AS completionRate` to keep response codes stable.
- Keep frontend component field usage and API examples as regression fixtures for backend response mapping.
- Add contract tests that compare old expected response schema with the new source-backed route for default, filtered, empty, and permission-limited states.

## Report Types And Execution Strategy

Classify the report before selecting API and execution behavior.

| Report Type | Backend Strategy |
| --- | --- |
| Fixed report | Stable SQL/template or generated query, strong parameter validation, cache, permission injection. |
| Configurable report | Metadata-driven dimension/metric/filter/sort whitelist, query planner, versioned publish/rollback. |
| Self-service analysis | Strict max dimension/metric/date/result limits, dataset whitelist, query grading, async or refusal for dangerous queries. |
| Detail report | Mandatory time or scope filters, bounded pagination, stable sort, field permissions, async export. |
| Summary/OLAP report | Governed metrics, aggregation pushdown, pre-aggregation/cache when useful, ratio numerator/denominator trace. |
| Realtime/high-frequency dashboard | Short TTL or precomputed cache, widget-level cache, source protection, stale last-success fallback. |
| Large export/report generation | Async job, batch query, streaming file write, isolated workers, retention, audit, retry/dead-letter. |
| Snapshot/reporting close report | Persisted snapshot/file for historical correctness, versioned result, audit and retention. |

## Metadata-Driven Query Contract

Prefer metadata-driven report definitions instead of one custom controller per report.

Minimum useful metadata includes:

- `report_definition`: report code/name/type, dataset, status, version, owner, cache TTL, timeout, max rows.
- `report_dataset`: source type, base table/view/query/API, datasource, dataset status, version, source grain.
- `report_dimension`: code/name, source expression, type, visibility, filterability, groupability, permission/sensitivity.
- `report_metric`: code/name, aggregate expression or metric reference, type, unit, format, additivity, owner.
- `report_filter`: code/name, source expression, operator whitelist, type, required/default, option source.
- `report_permission`: subject, report permission, data scope, field/export permission when separated.

Metric expressions and column expressions must be owned by backend configuration or a governed metric dictionary. User input may select codes only.

## Safe Query Rules

- Do not accept raw SQL, table names, column expressions, arbitrary operators, or arbitrary sort strings from the frontend.
- Map frontend codes to backend-owned metadata and reject unknown, hidden, non-filterable, non-groupable, or non-sortable fields.
- Use parameter binding for values. Never concatenate user values into SQL/source query strings.
- Inject tenant and data-permission predicates on the backend, not from frontend-supplied scope.
- Generate optional predicates according to the actual request. Avoid broad nullable-OR templates for high-volume endpoints.
- Apply global filters, permission scope, sorting, pagination, Top/Bottom, grouping, aggregation, and counts at the source/provider/repository/precompute/cache stage, not after full materialization in application memory.
- Apply `$performance-optimization` for database-backed endpoints and capture plan evidence for risky P0/high-volume queries.

## Parameter Guardrails

Every query endpoint must have explicit guardrails. Use project-specific limits, but do not leave the behavior open-ended.

- Required filters and defaults, especially time, tenant, organization, region, account, product, or dataset scope.
- Date/time range limits, expressed as left-closed/right-open ranges for timestamp queries when appropriate.
- Maximum dimension count, metric count, sort fields, `IN` values, keyword length, page size, page depth, returned rows, export rows, and file size.
- Query grade: light query can return synchronously; medium query may return synchronously with cache; heavy query goes async; dangerous query is rejected or requires approval.
- Error codes for invalid filters, heavy query, timeout, no permission, source unavailable, and export-limit exceeded.

## Permission And Cache Safety

Report permissions normally include menu, report, field, row/data-scope, export, admin/config, and subscription/snapshot permissions.

## Redis Role Matrix

When Redis is used, document one or more explicit roles rather than writing "use Redis cache":

| Redis Role | Good For | Required Contract |
| --- | --- | --- |
| Metadata/dictionary cache | Report definitions, dimension labels, enum dictionaries, filter options | Key template, report/source version, TTL, publish/rollback invalidation, stale tolerance. |
| Permission cache | Menu/report/field/data-scope summaries | Tenant/user/role dimensions, short TTL or permission-change invalidation, no cross-user sharing. |
| Result/widget cache | Expensive dashboard cards, KPI groups, chart series, table pages | Filter/version/permission/page/sort key dimensions, TTL+jitter, stampede protection, stale fallback, freshness metadata. |
| Canonical snapshot cache | Declared shared snapshot or materialized data cut | Snapshot role, grain, fields, version, permission scope, invalidation, consumers, and max value/row limits. |
| Rate/concurrency limit | Route/report/user/tenant throttling | Subject key, window, burst, TTL, overload response, observability. |
| Distributed lock/singleflight | Expensive cache rebuild or one-at-a-time refresh | Lock key, owner token, TTL, retry/wait behavior, unlock safety, timeout fallback. |
| Idempotency/job state | Export/report task creation, progress, short-lived status | Request hash, owner, terminal state, TTL, durable-store boundary, replay behavior. |

For every Redis role, also state connection-pool size, connect/read/write timeouts, retry/backoff, failure behavior, and metrics.

Redis should not replace the authoritative database/source for durable facts, audit logs, long-retention export records, or regulated state unless the project explicitly owns Redis persistence, backup, and recovery.

## Snapshot Role, Version Context, And Reuse

Snapshot/reporting-close semantics should be modeled as an explicit role plus a data-version contract, not guessed from the endpoint name.

- Snapshot/dashboard aggregate endpoints may return component-ready first-screen data for one data cut, expose a canonical/shared snapshot dataset, or both.
- The shared context is metadata such as `snapshotDate`, `latestPeriod`, `loadBatch`, `dataVersion`, report version, source version, tenant, permission hash, and filter values.
- Metrics, trends, rankings, tables, drilldowns, exports, and health endpoints may read from source queries, repository queries, precompute tables, Redis/cache entries, or a declared canonical snapshot filtered by that context.
- Declared snapshot reuse is valid when the contract documents matching grain, fields, filters, permission scope, version params, cache key, and invalidation behavior.
- Do not implement "call `/snapshot`, keep an undocumented payload in memory, then let `/metrics` read it" for production or production-like services.
- Application memory may hold bounded static definitions, whitelists, local ephemeral cache, or declared local/demo payloads only when the scope and correctness boundary are explicit. Production business data used across endpoints should be source-backed, precomputed, or stored in shared cache with explicit keys and invalidation.

## Parameter-Driven Query Context

Every data-bearing route should build a query context before reading business data:

- client-supplied stable params: report id, date/version filters, business filters, route/drilldown params, pagination, sorting, and keyword;
- backend-defaulted params: latest available snapshot date, latest period, load batch, data version, source partition, or report version when the client omits them;
- backend-injected scope: tenant id, user id, role/data-permission hash, organization/data-range predicates, field visibility, masking, and export permission;
- validated guardrails: allowed values, max date range, max page size, max `IN` size, sortable/filterable whitelist, and invalid-param behavior.

The query context must be passed into the repository/source/provider/precompute/cache layer. For database-backed endpoints, data-version, business filters, and permission scope map to SQL predicates or joins before aggregation, ranking, pagination, totals, and export. For precomputed or Redis-backed endpoints, the same values map to lookup keys or cache-key segments. Response metadata should echo the executed context; it must not be invented after an unscoped query.

Cache keys for report results and dashboard widgets must include all dimensions that can change the response:

- report id/code and report version
- dataset/source version or freshness partition
- snapshot date, latest period, load batch, data version, or equivalent data-cut identifier when relevant
- tenant id
- user/role/data-permission hash when data scope differs
- selected dimensions, metrics, filters, sorts, pagination, locale/unit/format, and feature flags

Never share permission-sensitive or tenant-scoped cache entries across users/tenants/roles. Export files also need tenant/user/report/task scoping and expiry.

Redis implementation notes:

- Use TTL jitter, request coalescing, singleflight, short locks, warmup, or precompute for expensive misses.
- Prefer bounded `MGET`/pipeline for multi-widget reads. Avoid `KEYS` and broad `SCAN` in request paths.
- Use Lua only for small atomic operations such as token buckets or conditional unlock.
- Bound serialized value size. Paginate, summarize, or precompute instead of caching huge result blobs.
- Return `fromCache`, `cacheAge`, `dataFreshnessTime`, `dataVersion`, and `stale` when cache freshness affects user trust.

## Endpoint Patterns

Use project naming conventions when available. Otherwise these report data-service endpoints are a stable starting point:

```http
POST /api/reports/{reportId}/query
GET  /api/reports/{reportId}/metadata
GET  /api/reports/{reportId}/filters
GET  /api/dashboards/{dashboardId}
POST /api/reports/{reportId}/exports
GET  /api/report-exports/{taskId}
GET  /api/report-exports/{taskId}/download
POST /api/admin/reports/{reportId}/publish
POST /api/admin/reports/{reportId}/rollback
POST /api/admin/reports/{reportId}/offline
GET  /api/admin/report-query-logs
GET  /api/admin/report-monitor/slow-reports
```

Dashboard endpoints may return a coherent widget group when widgets share filter scope, permission scope, refresh cadence, and lifecycle. Use widget-level cache internally when possible. Do not force the frontend to call many endpoints that repeatedly load the same metadata, permissions, dictionaries, or source data unless the split has a clear lifecycle or ownership reason.

If a dashboard endpoint is named `snapshot`, do not infer the role from the name alone. It may be a widget-group response, a canonical shared data cut used by trend/metric/table/export endpoints, or both. If other endpoints reuse it, document the reuse contract; otherwise those endpoints should receive or default the same version/scope params and query their own source/precompute/cache data.

## Result Shape

Report responses should be component-ready and self-describing enough for frontend integration and export consistency.

Include when applicable:

- `columns`: code, label/name, type, unit, precision, format, enum dictionary, sortable/filterable, sensitivity/masking.
- `rows`, `series`, `kpi`, `ranking`, `totals`, `subtotals`, or widget data needed by the component.
- `page`: page number/size, cursor, `hasNext`, total only when precise total is affordable and useful.
- `meta`: `fromCache`, query time, report version, data freshness time, data delay, data quality status/warnings, request id/trace id.

Data APIs should return data and metadata, not avoidable presentation composition. Prefer raw/structured facts and frontend-composable metadata:

- Good: `value`, `unit`, `precision`, `delta`, `trendDirection`, `thresholdLevel`, `reasonCode`, `messageKey`, `messageParams`, `columns`, `enumLabels`, `qualityWarnings`.
- Avoid: preassembled paragraphs, business conclusions, HTML/Markdown, rich text, style class names, combined value+unit strings, or strings such as `"完成率 85%，较上月提升 3%"` when the frontend can compose the same statement.

Server-owned text is acceptable only when it is part of a documented exception, such as error/no-permission messages, audit/legal/notification content, regulated explanation, or a governed/model-generated conclusion. When backend returns such text, also return structured evidence fields, variables, conclusion type, and status/confidence when applicable so frontend can still control styling and layout.

Do not leave KPI formulas, ranking, grouping, chart-series derivation, permission filtering, or multi-component splitting as implicit frontend work unless the exception is small, bounded, and documented. Conversely, do not move frontend copywriting, visual emphasis, layout wording, or style-specific conclusion assembly into the data service merely to make the first version easier.

## Export And Long-Running Work

Large exports and heavy report generation must not reuse the synchronous query route by adding `export=true`.

Export requirements:

- Create task -> return task id -> poll status/progress -> download result.
- Query and write in batches/streams. Do not load all rows into memory before writing a file.
- Run export in an isolated bounded worker pool and queue.
- Enforce max rows, max file size, timeout, retry/dead-letter policy, result retention, cleanup, and queue-full behavior.
- Recheck view/export/field/data permissions at task creation and result download.
- Audit who exported, report/version, filters, fields, row count, file, IP/device, download time, and failure reason.
- Apply masking, watermark, approval, expiry, and download-count limits for sensitive reports when required.

## Freshness, Quality, Precision, And Time

- Return or expose data freshness and quality status for production-bound report data. Users should know whether a number is realtime, hourly, daily, delayed, or from a stale fallback.
- Use decimal-safe numeric handling for money and ratios. Avoid floating-point rounding drift in financial or KPI outputs.
- Avoid premature rounding before aggregation. Format display precision at the response/metadata layer or final presentation layer.
- Ratio metrics should preserve enough lineage to explain numerator, denominator, zero-division behavior, and additivity.
- Define the business time field and timezone. Prefer left-closed/right-open timestamp ranges for date selection and state whether `dt` is business date, event date, payment date, refund date, completion date, or ingestion date.

## Multi-Tenant, Sensitive Data, And Audit

- Tenant isolation applies to queries, cache keys, export files, audit logs, datasource routing, and subscriptions.
- Sensitive fields need metadata such as sensitivity level, masking mode, export allowed status, and role exceptions.
- Audit query, export, download, report config change, permission change, datasource change, subscription, and snapshot behavior when in scope.
- Logs should store SQL hash, query id, redacted SQL/parameter summary, duration, row count, cache hit, status, and error summary. Do not log secrets, tokens, raw sensitive payloads, or full SQL with sensitive literals.

## Structured Backend Logging

Backend logging must be strong enough to diagnose production and integration failures without exposing sensitive data.

Minimum logging configuration:

- `LOG_LEVEL`: per environment, normally `debug` only in local/dev, `info` in test/prod, `warn/error` for noisy subsystems.
- `LOG_FORMAT`: `json` for test/prod and machine collection; console format is acceptable only for local development.
- `REQUEST_ID_HEADER`: accepted inbound request id header and generated fallback.
- `TRACE_ENABLED`: whether trace/span propagation is active.
- `SLOW_QUERY_MS` and `SLOW_REPORT_MS`: thresholds for source query and full report request warnings.
- `LOG_SAMPLE_RATE`: optional sampling for high-volume success logs; errors, warnings, validation rejects, auth rejects, export failures, and slow queries must not be sampled away.
- Redaction config: token/header names, password/secret keys, personal identifiers, raw SQL values, raw permission scopes, and large request/response bodies.

Required structured fields when available:

```text
timestamp, level, service, environment, releaseVersion,
requestId, traceId, spanId,
method, route, status, latencyMs,
tenantHash, userHash, roleHash,
reportId, widgetId, queryId, taskId,
snapshotDate, latestPeriod, loadBatch, dataVersion,
sourceName, cacheStatus, fromCache, stale,
page, pageSize, rowCount, exportRowCount,
poolName, poolActive, poolIdle, poolWaitMs,
errorCode, errorType, sanitizedMessage
```

Required log points:

- Request middleware: ingress and egress with request id, route, status, latency, and response error code.
- Auth/permission: successful scope resolution at debug/info when safe, and all auth/permission rejects at info/warn with reason code.
- Validation: rejected params, guardrail violations, heavy-query refusal, export-limit refusal, and no-permission response shape.
- Query context: report id, data-version fields, filter/sort/page hashes, permission hash, and query grade. Do not log raw sensitive filters.
- Query plan: selected dataset/source, metrics/dimensions codes, source predicate summary, pagination/count/export strategy, and cache key hash.
- SQL/source/upstream execution: start/end duration, row count, timeout/retry, upstream status, redacted SQL template or hash, and slow-query warnings.
- Cache/Redis: hit/miss/stale, key hash, TTL/freshness, rebuild/singleflight/lock behavior, and Redis errors.
- Connection pools: acquire wait, timeout, release on error path, saturation, active/idle counts when safe, and repeated failure non-exhaustion evidence.
- Export/jobs: task create/start/progress/success/failure/download/expiry with permission recheck and owner/request id.
- Data refresh: batch id/loadBatch, source freshness, row count, data quality warning, stale fallback, and failed refresh.
- Exceptions: error envelope correlation, sanitized message, stack trace only in controlled environments, and linked request id.

Logging anti-patterns:

- Raw tokens, cookies, access keys, database credentials, or SSO payloads.
- Full request/response bodies for report data.
- Full SQL with user values or sensitive literals.
- Unhashed user names, phone numbers, emails, ID numbers, or raw organization scope unless explicitly permitted by the project privacy policy.
- Only `print()` / `console.log()` statements without level, request id, route, or error code.
- Success-only logs with no warning/error path.
- Logs that state metadata such as `dataVersion` but cannot prove the source/precompute/cache query used that version.

## Monitoring And Governance

Track enough signals to govern report health after release:

- slowest reports, hottest reports, highest failure rate, highest export count, lowest cache hit rate
- average, P95, and P99 latency
- timeout count, query-too-heavy count, source unavailable count
- returned rows, scanned range when available, export rows/files
- cache hit ratio, stale fallback count, queue length, worker saturation, pool usage
- unused or deprecated reports for cleanup

Typical repairs include cache/precompute, query rewrite, summary table, query limit, async conversion, report split, dimension reduction, field removal, metric-governance repair, or report offline.

## Anti-Patterns

Treat these as findings unless explicitly scoped to a tiny non-production demo:

- API inventory lacks backend reuse pattern, common request model, response envelope, or service-layer mapping.
- Controller directly concatenates SQL or implements the full query chain.
- A new route/controller/DTO is created for every KPI/chart/table even though the metadata/filter/query/export/action family would fit.
- Frontend sends SQL, table names, column expressions, raw operators, or permission scope.
- Every report is a one-off controller with duplicated metric/filter/permission logic.
- All reports, exports, scheduled jobs, and heavy queries run synchronously in the default request pool.
- No required time/scope filter, unbounded page size, unbounded export, or unlimited `IN` list.
- Cache key omits tenant, permission scope, report version, dataset/source version, or user/role scope.
- Redis is mentioned without role, key template, TTL/invalidation, permission safety, miss/stampede behavior, fallback, pool/timeouts, and observability.
- Redis request path uses `KEYS`, unbounded `SCAN`, huge values, infinite TTL for mutable data, or distributed locks without TTL/owner token.
- Data API returns avoidable concatenated display text, conclusions, HTML/Markdown, or style-implied strings instead of structured facts and metadata, making frontend styling, localization, responsive layout, or emphasis control difficult.
- Metrics, trends, rankings, tables, exports, or drilldowns read an undocumented snapshot/dashboard API response or application-memory snapshot as their data source instead of using a declared snapshot/source/precompute/shared-cache contract by data-version context.
- Response metadata echoes `snapshotDate/dataVersion` or scope values, but the repository/source/precompute/cache query did not use those values as params, predicates, or key segments.
- Query/export opens a new physical database connection per request instead of using a bounded pool.
- Query/export/repository code acquires a pooled connection and can raise `ApiError`, timeout, cancellation, or another exception before release/close. Success-path-only cleanup is a connection leak; for small pools such as `STARROCKS_POOL_MAX=5`, this is a production blocker.
- Export loads all rows into memory before writing.
- Core metrics are recalculated differently by each report.
- No audit log for sensitive query/export/download/config changes.
- Report configuration changes take effect in production without draft/preview/publish/version/rollback controls.

## Readiness Rules

Mark report data-service backend readiness:

- `ready`: metadata, parameter-driven query context, query chain, snapshot role/reuse rule, data-version context, permissions, parameter guardrails, source mapping, API/result contract, cache/export, audit, freshness/quality, SQL strategy, performance/resilience, environment, and production handoff decisions are confirmed, documented or implemented, and testable for the stated scope.
- `partial`: local/demo/test scope can proceed with named limitations, or production scope lacks non-blocking controls such as complete monitoring, warmup, snapshot, subscription, or slow-report governance.
- `blocked`: the service would accept unsafe SQL/source inputs, has unknown source authority or metric口径, relies on undocumented data-bearing endpoint-to-endpoint runtime dependencies, lacks data-version context or snapshot reuse rules for snapshot/latest-period semantics, cannot show how data-version/business/permission scope params constrain source/precompute/cache/snapshot queries, lacks permission/tenant isolation, lacks bounded pagination/export, keeps risky heavy work synchronous, has no cache-permission safety, lacks required audit for sensitive data, or cannot document how global filters/query limits execute before response construction.

## Handoff Evidence

Backend/API documentation, implementation notes, and validation reports should include:

- Upstream technical-solution linkage: consumed `ARC-*`, `ADR-*`, `API-*`, `LGM-*`, `NFR-*`, `GAP-*`, and any divergence from them.
- Data-service boundary and layered architecture: controller, service/use-case, metadata, query planner, source adapter, formatter, cache/precompute, export, permission, observability, and runtime ownership.
- Report type and execution strategy.
- Backend API family/reuse pattern for each endpoint.
- Metadata model or explicit reason why a fixed endpoint is acceptable.
- Query chain ownership and layer mapping.
- QueryContext contract: client params, backend defaults, data-version fields, backend-injected tenant/permission scope, guardrails, and source/cache/precompute mapping.
- Endpoint list with served component/widget group.
- Request guardrails and error codes.
- Permission, tenant, field masking, and export-permission behavior.
- Source-adapter compatibility matrix when table/upstream/fixture/source changes.
- Data-vs-presentation boundary: structured data/metadata returned by backend, frontend-owned copy/conclusion composition, and documented server-owned text exceptions.
- Cache key dimensions, TTL, invalidation, warmup, stale fallback, and permission safety.
- Redis role matrix and operational contract when Redis is used.
- Database/upstream connection lifecycle evidence: pool max config such as `STARROCKS_POOL_MAX`, acquire/release owner, `ApiError`/timeout/exception cleanup path, and repeated-failure proof that the pool is not exhausted.
- Structured logging evidence: logger config, request/trace middleware, required fields, redaction rules, log levels, request/auth/validation/query/cache/pool/export/job/error log points, slow-query/report thresholds, and error-envelope correlation.
- Code file ledger evidence for changed backend code: sidecar ledger path, pre-change read/create proof, appended version, changed route/service/repository/query/logging ranges, affected API/env/source/permission contracts, verification, and rollback notes.
- Pagination/count/export strategy.
- Async export/job lifecycle evidence when applicable.
- Result metadata for columns, precision, freshness, quality, cache status, and trace id.
- Audit and monitoring evidence.
- Environment/source-mode evidence, health/readiness path, deployment and rollback notes for production-bound work.
- Linked `$performance-optimization` findings or pass status.
