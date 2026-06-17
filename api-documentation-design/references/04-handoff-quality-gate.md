# Handoff Quality Gate

Use this reference before delivering the API document or handing it to frontend, backend, QA, or downstream documentation work.

## Readiness Checks

- Every expected endpoint is documented or explicitly removed with a reason.
- Common conventions are defined before endpoint details.
- Each endpoint has method, path, purpose, trigger, auth, request parameters, response schema, examples, errors, performance notes, status, and pending items.
- Each data-bearing endpoint identifies the component or justified component group it serves.
- Each production-bound endpoint identifies backend reuse pattern, common request model, response envelope/model family, and service-layer mapping, or explains why a custom shape is required.
- Each response schema traces to implementation, model/source, upstream API, frontend contract, or explicit design decision.
- When source table/view/upstream/fixture replacement is planned or has occurred, existing response fields remain stable and new fields are additive, conventionally named, source-traced, permission-aware, and documented with compatibility status.
- Each transformation rule is documented inline, linked to a local transformation note, or marked with `TBD(GAP-*)` plus owner/impact.
- Each missing decision is recorded in pending items with a stable `GAP-*` ID, owner question, impact, and blocking status.
- Endpoint examples are usable by frontend integration and integration-test case design.
- Error and empty-state shapes are consistent across endpoints.
- Pagination, sorting, filtering, export, and drilldown rules use stable names and defaults.
- Global/page-level filters for database-backed endpoints are mapped to SQL `WHERE` or equivalent source/provider predicates; component-internal local filters are explicitly scoped to already fetched component datasets.
- Report/BI/dashboard endpoints document report type, metadata or fixed-contract source, dimension/metric/filter/sort whitelists, frontend-code-only input rule, backend-owned SQL/source mapping, parameter guardrails, backend-injected tenant/data/field/export permissions, component-ready result metadata, freshness/quality, cache key permission safety, async export lifecycle, query/export/download audit, and slow-report governance when relevant.
- Snapshot/latest-period and other versioned data endpoints document snapshot role/reuse and parameter-driven version/scope filtering: request/defaulted/injected params, declared reusable snapshot source when applicable, source/provider predicates or precompute lookup keys, Redis/cache key dimensions, and proof that response metadata is based on the executed query context.
- Database-backed endpoints document SQL pushdown scope, selected-column/projection rule, direct/type-consistent predicate mapping, index support, join keys/cardinality, dedup/order necessity, pagination/keyset strategy, aggregation/window placement, dynamic optional-filter behavior, plan-evidence need, and any non-sargable filter blockers.
- Endpoints document the execution stage for filters, sorting, pagination, ranking, Top/Bottom, grouping, aggregation, and counts; any full-materialize-then-filter behavior is `partial` or `blocked` unless the input is a documented tiny static enum or bounded lookup.
- Database-backed implementation handoff documents connection-pool behavior or confirms the runtime/project already owns pooling.
- Production-bound data-service handoff documents bounded concurrency/thread/worker behavior or confirms the runtime/project already owns concurrency safely.
- Redis/cache behavior is documented when used for hot or expensive queries, including key dimensions, TTL, invalidation, permission safety, and fallback.
- Upstream-dependent endpoints document timeout, retry/backoff, circuit-breaker or failure-threshold behavior, fallback/degraded response shape, and upstream owner/SLA when known.
- Expensive endpoints document rate/concurrency limits, request-size/export limits, overload behavior, and async/offline strategy when synchronous response is risky.
- Collection/list/table endpoints document bounded pagination, default/max page size, stable sorting, total-count behavior, and large-result/export handling.
- Backend/API implementation handoff that needs mock data uses SQLite fixture databases for simulation; JSON files are response examples only, not data sources.
- Frontend compute policy is explicit. APIs should return component-ready values, series, rows, totals, ranks, and formula fields; any frontend-side business calculation exception is bounded and documented.
- Data-vs-presentation boundary is explicit. Data APIs should avoid backend-assembled display copy, business conclusion paragraphs, HTML/Markdown, combined value+unit strings, or style-implied labels; return structured facts, metadata, codes, `messageKey`, and `messageParams` unless a server-owned text exception is documented.
- Async jobs, callbacks, webhooks, streams, imports, or exports have lifecycle, status/progress, cancellation when allowed, queue/worker limits, retry/dead-letter behavior, idempotency, retention/expiry, result download/callback behavior, and failure behavior documented when relevant.
- Production-bound documents include source authority, runtime environment profile notes, auth/permission behavior, health/runtime evidence, observability, performance/resilience/export limits, version compatibility, and testing handoff.

## Status Labels

- `ready`: enough detail exists for implementation, frontend integration, and tests.
- `partial`: usable with documented assumptions or limited behavior.
- `blocked`: missing source, permission, model, auth, environment profile, or business rule prevents reliable implementation/integration.
- `deprecated`: retained for compatibility but not recommended for new use.

For production-bound delivery, do not use `ready` when source authority, auth/permission, backend reuse pattern/model-family mapping, report data-service backend behavior when report APIs are in scope, response-field compatibility for source/table replacement, parameter-driven version/scope filtering for versioned data endpoints, `.env.production` profile/base URL evidence, runtime/health evidence, observability, performance/resilience/export limits, SQL query strategy for database-backed endpoints, version compatibility, or testing handoff is missing.

## Handoff Summary

End delivery with:

- Ready endpoint count.
- Partial endpoint count and assumptions.
- Blocked endpoint count and exact blockers.
- Production closed-loop readiness and missing controls when applicable.
- Required owner confirmations.
- Suggested next validation activity, such as backend contract validation, frontend contract validation, or integration-test design, described as a handoff note rather than a prerequisite skill call.
