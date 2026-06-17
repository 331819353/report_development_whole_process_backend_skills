---
name: olap-data-modeling-optimization
description: "[后端阶段] 本阶段版本仅服务后端/数据服务设计、API文档/契约、接口实现、运行验证和后端交付；不承接原型设计、前端代码或测试执行。用于OLAP建模、分析查询服务模型、星型/宽表/聚合表/物化视图、事实维度粒度、预聚合、StarRocks/ClickHouse类分析库、指标聚合与服务层性能优化。用户提到OLAP建模、宽表设计、星型模型、预聚合、物化快照、汇总表、分析查询慢、指标服务模型、事实表维度表时触发；不替代API文档或具体SQL单句优化。"
---

# OLAP Data Modeling Optimization

## Stage Scope

Classification: 后端阶段.

Use this copy only inside the backend/data-service skill bundle. Treat frontend, prototype, and testing work as contracts, evidence, handoff notes, or blockers; do not edit those stages from this skill.

## Positioning

Use this skill when performance or correctness depends on analytical data modeling rather than one query rewrite: process/grain, fact and dimension design, serving models, pre-aggregation, materialized snapshots, and metric aggregation strategy.

Use `$sql-query-optimization` for a specific SQL/query-shape problem. Use `$performance-optimization` for full API/cache/frontend/export performance diagnosis.

## Reference Loading

- Read `references/olap-data-modeling-optimization.md` before designing or accepting OLAP/report serving models.

## Anti-Laziness Gate

For non-trivial work, apply `$quality-gate-validation` `references/anti-laziness-execution-gate.md` before final output, handoff, or readiness. Do not mark the result ready while `LAZY-*` findings remain open, when available local evidence was not inspected, when owning skills were skipped, or when proof is limited to generic statements such as "checked", "optimized", "looks good", or "implemented".

## Workflow

1. Identify business process, report type, metrics, dimensions, grain, freshness, volume, and query patterns.
2. Choose serving model: raw fact + dimensions, wide table, aggregate table, materialized view, snapshot/precompute, or hybrid.
3. Define metric additivity, numerator/denominator rules, slowly changing dimensions, late-arriving data, and data-version behavior.
4. Align model with API/query-service needs: filters, sorting, TopN, drilldown, export, permission scope, and cache/precompute.
5. Define validation: row counts, reconciliation, freshness, query plans, and performance targets.

## Required Output

- OLAP model choice and rationale.
- Grain, fact/dimension/aggregate/snapshot design.
- Metric aggregation and data-version rules.
- Query/API/cache implications.
- Verification and readiness.

## Quality Gate

- Do not choose a wide table, preaggregate, or snapshot that hides metric口径, denominator, permission scope, or drilldown requirements.
- Do not mark OLAP modeling ready without grain, freshness, source authority, reconciliation, and serving-query evidence.
