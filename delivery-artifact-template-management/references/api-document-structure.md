# Document Structure

Use this reference when creating the API document skeleton.

## Recommended Structure

0. Human-readable summary
   - Who will consume this API document.
   - Main modules/endpoints covered.
   - Current readiness: ready, partial, or blocked.
   - Critical blockers, assumptions, and next owner actions.
1. Document metadata
   - Title, version, date, owner, status, environment profile/config file, related artifacts, and change notes.
2. Common conventions
   - `.env.test`/`.env.production`, base URL, versioning, auth, headers, response envelope, error envelope, pagination, sorting, filtering, date/time, enums, file upload/download, idempotency, report data-service backend conventions, async/offline job conventions, concurrency/cache/pool/timeout/retry/fallback, SQL query conventions for database-backed APIs, and rate/performance-resilience limits.
3. Endpoint overview table
   - API id, module/domain, name, method, path, purpose, auth, response model, priority, status, and pending items.
   - Add one plain-language sentence before the table that explains the endpoint group and frontend/backend consumer.
4. Endpoint details
   - Full detail for each endpoint. Use `$api-documentation-design` for endpoint-level request, response, auth, error, performance, and compatibility rules.
5. Model and dependency trace
   - Response models, source models, upstream systems, transformation notes, formulas, refresh cadence, data quality assumptions, and permission dependencies.
6. Production closed-loop readiness
   - Source authority, runtime/base URL, auth/permission behavior, `.env.test`/`.env.production` notes, health/runtime evidence, observability, performance/resilience/export constraints, compatibility/versioning, testing handoff, readiness, and blockers.
7. Appendix
   - Enums, error codes, common examples, unresolved items, glossary, and compatibility notes.

## Grouping Options

- By page/module when APIs are consumed by frontend pages or report modules.
- By domain/resource when APIs are REST-like or service-owned.
- By workflow step when APIs support a business process.
- By bounded service when documenting multiple backend services.
- By interaction style when documenting synchronous APIs, async jobs, webhook/callbacks, streaming/SSE, batch imports, or file exports.

## Common Convention Checklist

- Base URL per environment profile: `.env.test` and `.env.production` when data-service delivery is in scope.
- Auth headers and token refresh/expiration behavior.
- Common request headers such as trace id, locale, tenant, app id, or client id.
- Common response envelope, including success and failure examples.
- Error envelope with HTTP status, business code, message, detail, trace id, and recoverability.
- Pagination names, defaults, maximums, and total-count behavior.
- Sorting syntax, allowed sort fields, and default sort.
- Filter syntax, date range inclusivity, timezone, enum values, and default filters.
- File upload/download content type, filename, streaming, and export size limits.
- Report data-service backend conventions for report/BI/dashboard APIs: report type, metadata/fixed-contract source, dimension/metric/filter/sort whitelist, frontend-code-only rule, backend-owned source/SQL mapping, parameter guardrails, permission injection, component-ready result metadata, freshness/quality, cache safety, export lifecycle, audit, versioning, and slow-report governance.
- Data-service performance/resilience conventions: expected volume/latency, concurrency model, cache/precompute, resource pools, `ApiError`/timeout/exception connection release/close behavior, async/offline job strategy, timeout/retry/fallback, rate/concurrency limits, and observability.
- SQL query conventions for database-backed APIs: selected columns, sargable predicates, join cardinality, pagination/keyset strategy, aggregation/window placement, dynamic optional-filter strategy, and plan-evidence expectation.
- Async job, callback, webhook, streaming, or batch-processing conventions when relevant, including status/progress, cancellation, queue/worker limits, retry/dead-letter behavior, idempotency, result retention, and failure states.
- Backward compatibility and deprecation notes.
- Production-bound docs include `.env.production` profile/base URL, health/runtime evidence, source authority, auth/permission, observability, performance/resilience/export limits, testing handoff, and blockers.
