---
name: sql-query-optimization
description: "[后端阶段] 本阶段版本仅服务后端/数据服务设计、API文档/契约、接口实现、运行验证和后端交付；不承接原型设计、前端代码或测试执行。用于SQL查询写法、索引友好条件、分页排序、聚合、JOIN、可选筛选、执行计划和慢查询优化。用户提到SQL慢、查询优化、索引没走、where条件、order by慢、group by慢、分页慢、TopN、count慢、执行计划、StarRocks/MySQL/Oracle查询写法优化时触发；不负责Redis缓存或完整API性能治理。"
---

# SQL Query Optimization

## Stage Scope

Classification: 后端阶段.

Use this copy only inside the backend/data-service skill bundle. Treat frontend, prototype, and testing work as contracts, evidence, handoff notes, or blockers; do not edit those stages from this skill.

## Positioning

Use this skill for SQL/query-shape optimization and database-backed report/API query review. It owns predicate shape, projection, minimal source-query boundaries, joins/aggregation exception checks, pagination, sort, count, plan evidence, and safe parameter binding.

For interface implementation, default to source-query-simple: inspect table content first, map request params to predicates, query selected rows, and avoid joins, aggregation, exact counts, formulas, totals, rankings, and broad post-processing unless a derived/summary exception is documented.

Use `$performance-optimization` when the performance surface also includes API design, cache, export, frontend rendering, capacity, or end-to-end verification.

## Reference Loading

- Read `references/sql-query-writing-optimization.md` before proposing or accepting SQL/query-shape optimizations.

## Anti-Laziness Gate

For non-trivial work, apply `$quality-gate-validation` `references/anti-laziness-execution-gate.md` before final output, handoff, or readiness. Do not mark the result ready while `LAZY-*` findings remain open, when available local evidence was not inspected, when owning skills were skipped, or when proof is limited to generic statements such as "checked", "optimized", "looks good", or "implemented".

## Workflow

1. Identify database/dialect, query purpose, result grain, source table(s), filters, sort, pagination, volume, and SLA.
2. Inspect table-content evidence, request-param-to-source-field mapping, SQL/query builder shape, and available plan evidence.
3. For source-query-simple APIs, optimize selected columns, predicates, stable sorting, pagination, and optional filter handling while keeping aggregation/join/formula work absent.
4. For approved derived/summary endpoints, optimize joins, aggregation/window placement, Top/Bottom, count strategy, and precompute/source-table choices.
5. Preserve metric formulas, permission predicates, source-side filtering, and response compatibility.
6. Define verification: table evidence, `EXPLAIN`, query timing, row counts, before/after plan, and correctness checks.

## Required Output

- Query surface and bottleneck hypothesis.
- Minimal implementation mode, table-content evidence, and request-param-to-source-field mapping.
- SQL/query rewrite or review findings.
- Index/predicate/page/sort/aggregation notes.
- Correctness and permission-scope risks.
- Verification result or blocker.

## Quality Gate

- Do not optimize by changing metric口径, permission scope, business totals, filters, or response semantics.
- Do not approve a source-query-simple API that uses hidden filters, uninspected tables, joins, aggregation, exact counts, formulas, totals, rankings, or broad in-memory post-processing.
- Do not fetch broad result sets and filter/sort/page globally in memory for database-backed data.
- Use parameter binding and whitelisted fields; never concatenate user-controlled SQL.
