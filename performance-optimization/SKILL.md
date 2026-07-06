---
name: performance-optimization
description: "[后端阶段] 本阶段版本仅服务后端/数据服务设计、API文档/契约、接口实现、运行验证和后端交付；不承接原型设计、前端代码或测试执行。用于报表、API、SQL、数据服务和前端可视化性能优化。用户提到接口慢、SQL慢、查询优化、索引、分页、缓存、Redis、Redis使用技巧、缓存击穿/穿透/雪崩、TTL、分布式锁、限流、连接池、并发、首屏慢、snapshotDate/dataVersion/loadBatch、快照接口优化、图表卡顿、表格大数据、导出慢、渲染性能、ECharts 性能、OLAP 建模、生产性能压测或容量限制时触发。"
---

# Performance Optimization

## Stage Scope

Classification: 后端阶段.

Use this copy only inside the backend/data-service skill bundle. Treat frontend, prototype, and testing work as contracts, evidence, handoff notes, or blockers; do not edit those stages from this skill.

## Positioning

Use this skill to design, review, or repair performance-sensitive behavior across data services, SQL/OLAP, APIs, frontend data loading, charts, tables, exports, and runtime rendering.

It owns performance strategy and verification. It does not replace API design, data modeling, frontend implementation, or testing workflows.

For interface implementation, performance optimization must respect the minimal source-query default: inspect table content first, keep filters as request params mapped to source predicates, and do not introduce joins, aggregation, exact counts, formulas, totals, rankings, cache-derived hidden state, or broad in-memory processing into a simple retrieval endpoint unless an approved derived/summary/precompute exception exists.

## Reference Loading

- Data service resilience, cache, pagination, pooling, and capacity: `references/data-service-performance-resilience-contract.md`
- Redis cache, lock, rate-limit, job-state, and hot-query usage patterns: `references/redis-cache-usage-patterns.md`, then `$redis-cache-design-patterns` when deeper cache design is needed.
- SQL query writing, execution shape, and index-friendly filters: `references/sql-query-writing-optimization.md`, then `$sql-query-optimization` when query-specific repair is needed.
- OLAP modeling and analytical aggregation: `references/olap-data-modeling-optimization.md`, then `$olap-data-modeling-optimization` when model redesign is needed.

## Anti-Laziness Gate

For non-trivial work, apply `$quality-gate-validation` `references/anti-laziness-execution-gate.md` before final output, handoff, or readiness. Do not mark the result ready while `LAZY-*` findings remain open, when available local evidence was not inspected, when owning skills were skipped, or when proof is limited to generic statements such as "checked", "optimized", "looks good", or "implemented".

## Workflow

1. Identify the performance surface: SQL/source, API, backend service, cache, export, frontend fetch/adaptation, chart/table rendering, or deployment runtime.
2. Define performance target: latency, throughput, first screen, interaction time, export time, row count, concurrency, freshness, or memory budget.
3. Locate current bottleneck evidence: query plan, network waterfall, API logs, browser performance trace, data volume, component count, or user report.
4. Select the data-service performance pattern before using Redis or async work: source-side query optimization, precompute/materialized snapshot, Redis cache, stale fallback, request coalescing, rate/concurrency limit, async job, or frontend rendering optimization.
5. Apply the smallest appropriate optimization. For source-query-simple APIs, prefer projection/predicate/range rewrite, pagination/keyset, connection-pool safety, and request bounds. Use aggregation pushdown, cache, or precompute only as explicit derived/summary exceptions with correctness and permission evidence.
6. Define verification commands, metrics, before/after evidence, and residual risk.

## Required Output

- Performance surface and target.
- Bottleneck evidence and hypothesis.
- Minimal interface impact: whether the endpoint remains source-query-simple or has a documented derived/summary/precompute exception.
- Optimization plan or implemented changes.
- Redis/cache/precompute decision when relevant: key template, TTL/invalidation, permission-safety dimensions, stampede protection, fallback, and observability.
- Risks around correctness, freshness, permission scope, cache invalidation, and export completeness.
- Verification result or blocker.

## Quality Gate

- Do not optimize by changing metric口径, permission scope, or business totals.
- Do not optimize a simple table retrieval endpoint by adding hidden joins, aggregation, exact counts, formulas, totals, rankings, cache-derived hidden state, or broad post-processing.
- Do not fetch broad result sets and filter/sort/page globally in memory for database-backed data.
- Do not optimize request count by making one data API a hidden runtime source for another. Snapshot/dashboard aggregate APIs, metrics, trends, tables, and exports may share `snapshotDate/latestPeriod/loadBatch/dataVersion`, cache invalidation, and a declared canonical/shared snapshot; undocumented endpoint-payload reuse is the risk, not explicit snapshot reuse.
- Do not optimize by removing or ignoring backend query params. Data-version, business filters, pagination/sort, and permission/data scope must remain source-side predicates, precompute lookup inputs, or cache-key dimensions.
- Cache keys must include filters, permission/user/tenant scope, source version, pagination/sort, and locale/unit options when relevant.
- Redis usage is not ready when key dimensions, TTL/invalidation, permission safety, miss/stampede behavior, fallback, pool/timeouts, and observability are unknown.
- Database/upstream connection-pool usage is not ready when any query path can raise `ApiError`, timeout, cancellation, validation error after acquire, early return, or generic exception without releasing/closing the acquired connection in `finally`, context-manager cleanup, or an equivalent pool-safe guard. A leaked StarRocks connection can exhaust a small pool such as `STARROCKS_POOL_MAX=5`; treat this as a blocker, not a minor resilience issue.
- Frontend rendering optimizations must preserve loading, empty, error, and interaction states.
