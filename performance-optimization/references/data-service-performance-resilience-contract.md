# Data Service Performance And Resilience Contract

Use this shared contract whenever a data service, backend API, API inventory, API document, implementation handoff, or production-readiness review must support real users, production-like data volume, or stable integration testing.

Performance and stability are design concerns, not late implementation details. A data service is not production-ready just because routes return the right fields.

For report/BI/dashboard backends, apply `$backend-development-workflow` alongside this contract so metadata, permissions, parameter guardrails, query planning, component-ready responses, async export, audit, freshness, and slow-report governance are covered in addition to generic performance controls.

When Redis is named, also apply `$redis-cache-design-patterns`. Redis decisions must include role, key template, TTL/invalidation, permission-safety dimensions, miss/stampede behavior, fallback, pool/timeouts, and observability.

## Required Design Dimensions

For every production-bound data service, record the applicable decisions below or mark them explicitly out of scope with a reason.

| Dimension | Required Decision |
| --- | --- |
| Latency and capacity target | Expected QPS/concurrency, p50/p95/p99 latency target, data volume, request size, export size, and peak/normal traffic assumption. |
| Concurrency model | Thread pool, async/non-blocking IO, worker/process count, queue length, backpressure, and CPU-bound vs IO-bound handling. |
| Resource pools | Database pool, Redis/cache pool, HTTP/upstream client pool, min/max size, acquire/connect/read timeout, idle timeout, validation, and safe shutdown. |
| Cache/precompute | Redis/project cache/in-memory bounded cache/precompute choice, role, key dimensions, TTL, invalidation, warmup, permission/user/tenant safety, stampede protection, stale/fallback behavior, hit-rate metric, and operational fallback. |
| Query execution | Source-side filtering/sorting/pagination/aggregation, index strategy, total-count strategy, cursor/keyset need, slow-query risk, and no full-materialize-then-filter behavior for global scope. |
| Async/offline processing | Job/task need, queue/worker owner, job status API, progress, cancellation, retry/dead-letter behavior, result retention, idempotency, timeout, and user notification or download behavior. |
| Upstream resilience | Timeout, retry with backoff/jitter, circuit breaker, bulkhead/isolation, fallback/degraded response, idempotency, and upstream SLA/owner. |
| Traffic protection | Rate limit, concurrency limit, request body limit, export async/offline strategy, queue limit, overload response, and abuse protection. |
| Health and readiness | Liveness, readiness, representative dependency checks, pool saturation checks, and startup/shutdown behavior. |
| Observability | Request ID, logs, metrics, traces, latency percentiles, error rate, timeout/retry count, cache hit ratio, pool usage, queue length, slow query, and alert owner. |
| Failure behavior | Empty/error/no-permission/upstream-failed/cache-stale/degraded response shape and whether partial data is allowed. |

## Concurrency Rules

- Use bounded concurrency. Do not create unbounded threads, promises, goroutines, workers, or queues for request handling.
- Choose the concurrency model according to workload type: IO-heavy routes may use async/non-blocking IO or bounded worker pools; CPU-heavy calculations should use bounded workers, precompute, or offline jobs instead of blocking request threads.
- Document pool/worker ownership when the framework already manages it, such as servlet containers, ASGI workers, Node event loop plus worker threads, or Java executor pools.
- Backpressure must be explicit: queue limit, timeout, rate limit, or overload response. Silent queue growth is a stability risk.

## Async Processing Rules

- Use async/offline processing for long-running exports, heavy report generation, batch imports, expensive aggregation, multi-upstream fan-out, retryable side effects, or work that may exceed the synchronous latency target.
- Synchronous endpoints must have bounded work and a hard timeout. If expected work can exceed the accepted timeout or normal request-thread budget, return a job/task ID instead of holding the request open.
- Async contracts must document job creation, job ID, status/progress query, terminal states, cancellation when allowed, retry/replay behavior, result download or callback, result retention/expiry, permission checks, and error shape.
- Use idempotency keys or deduplication for job creation when duplicate submissions are possible.
- Workers must be bounded and isolated from request threads. Record worker count, queue limit, scheduling priority, timeout, retry policy, dead-letter handling, and overload behavior.
- Do not let async queues grow silently. Expose queue-full or rate-limit behavior, and keep job acceptance separate from job completion.
- Result storage must document sensitivity rules, tenant/user scoping, expiry, cleanup, and whether partial results are allowed.
- Polling and callback/webhook behavior must include recommended polling interval, callback auth/signature when applicable, duplicate event handling, and failed-delivery retry/dead-letter rules.
- Observability must cover job creation rate, queue length, queue wait time, running jobs, worker saturation, job latency, success/failure/retry count, dead-letter count, and result download failures.

## Cache Rules

- Cache keys must include every value that changes the response: global filters, permission scope, user/tenant/role when relevant, pagination/sort, source version, locale/unit, and feature flags.
- For snapshot/latest-period report APIs, cache keys must include the shared data cut such as `snapshotDate`, `latestPeriod`, `loadBatch`, `dataVersion`, report version, or source version.
- Business filters and backend-injected permission/data scope must be included in precompute lookup keys or cache-key dimensions whenever they change the returned data.
- Permission-sensitive or personalized data must not be shared across users/tenants/roles through cache keys.
- Expensive cache misses need stampede protection such as lock, singleflight, request coalescing, jittered TTL, warmup, or precompute.
- Cache invalidation must name the event, schedule, source version, manual operation, or TTL that makes stale data acceptable.
- In-memory cache is allowed only for bounded local state or single-instance scope. Production multi-instance services should prefer shared cache or document why local cache is safe.
- In-memory cache must not become an undocumented cross-endpoint source of truth. Do not optimize by storing an unscoped snapshot/dashboard API payload in memory and having metrics/trend/table/export endpoints read it. Use a declared canonical/shared snapshot, shared cache, precompute, or source query keyed by the data-version context instead.
- Redis is acceptable for metadata/dictionary cache, permission summaries, result cache, dashboard/widget cache, canonical snapshot cache, rate limiting, distributed lock, idempotency key, and short-lived job progress. For each role, document key template, value type, TTL, invalidation, max value size, miss behavior, fallback, and metrics.
- Avoid Redis request-path operations that do not scale: unbounded `KEYS`, broad `SCAN`, large value blobs without size limits, infinite TTL for mutable data, and locks without TTL/ownership token.
- Prefer `MGET`/pipeline for bounded multi-key reads and Lua only for small atomic operations such as counters, token buckets, or conditional unlocks.

## Resource Pool Rules

- Database-backed APIs must use a connection pool or document that the runtime/framework owns pooling externally.
- Every acquired database/upstream connection must be released or closed on all paths. Use a context manager, `try/finally`, `defer`, `using`, or equivalent guard around the exact acquire scope; do not rely on normal success-path code after query execution.
- `ApiError` and framework/business exceptions are not allowed to bypass pool cleanup. If a query raises `ApiError`, timeout, cancellation, validation error after acquire, formatter error, early return, or any generic exception, the connection must still be returned to the pool or closed before the error envelope is produced.
- For StarRocks or similar small pools, record the max pool config such as `STARROCKS_POOL_MAX` and test the failure path. With a default max such as `STARROCKS_POOL_MAX=5`, repeated `ApiError` leaks can exhaust the pool and make later requests fail to create/acquire connections.
- Redis clients must use bounded pools, connect/read/write timeouts, retry/backoff limits, and safe shutdown behavior.
- Upstream HTTP/API clients should reuse connections and define connect/read/overall timeout.
- Pool limits must be consistent with database/upstream limits and application worker count; increasing threads without pool limits can reduce stability.
- Health checks should not exhaust pools or run expensive dependency probes on every request.

## Query Execution Rules

- For database-backed APIs, apply `$sql-query-optimization` alongside this contract.
- Global/page-level filters, permission scope, sorting, pagination, grouping, aggregation, Top/Bottom, and counts should execute at the source/provider/repository/precompute/cache stage rather than after full materialization in application memory.
- Endpoint batching, dashboard snapshots, and request-count reductions must preserve explicit dependency contracts. Shared data-version context, shared precompute tables, and declared canonical snapshots are acceptable; hidden endpoint-to-endpoint payload dependency is not.
- Data-version, business filters, and permission/data scope must remain explicit query inputs. Optimizing by using a default snapshot, broad cache entry, or response metadata echo without parameterized filtering is a correctness regression.
- Risky P0 or high-volume queries need SQL query-shape notes and plan evidence or an explicit slow-query gap.

## Readiness Rules

- Mark data-service/API design `ready` only when applicable performance and resilience decisions are documented or explicitly out of scope.
- Mark `partial` when the service can run for local/demo/test scope but lacks confirmed capacity, latency, pool, cache, async/offline, SQL plan, timeout, or observability decisions.
- Mark `blocked` when a production-bound endpoint may overload the source, uses unbounded concurrency, accepts unbounded async queue growth, lacks source-side filtering/pagination for large data, opens one connection per request, can leak pooled database/upstream connections on `ApiError`/timeout/exception paths, uses Redis without key/TTL/invalidation/permission-safety/miss/fallback/pool decisions, depends on another endpoint's in-memory response payload for correctness, omits data-version/business/permission scope from query or cache keys, has no timeout/failure behavior for required upstream dependencies, or keeps long-running work synchronous without a safe limit.

## Handoff Evidence

For implementation, validation, or production acceptance, include:

- Endpoint-level performance/resilience table.
- Config keys or files for pool, Redis/cache, timeout, worker, and rate-limit settings.
- Connection lifecycle evidence for database/upstream pools: acquire/release ownership, `ApiError`/timeout/exception cleanup path, pool max such as `STARROCKS_POOL_MAX`, and a repeated-failure test proving the pool is not exhausted.
- Redis handoff evidence when used: role, key template, TTL/invalidation, permission-safety dimensions, miss/stampede behavior, fallback, pool/timeouts, and metrics.
- Async job contract and evidence when long-running work exists: create/status/cancel/result endpoints, queue/worker limits, retry/dead-letter policy, retention, and sample job lifecycle.
- Load/smoke evidence when available: request count, latency, error rate, saturation, cache hit ratio, and slow-query sample.
- Open performance risks with owner, impact, current assumption, and next verification step.
