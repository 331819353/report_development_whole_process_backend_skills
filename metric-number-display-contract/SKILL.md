---
name: metric-number-display-contract
description: "[后端阶段] 本阶段版本仅服务后端/数据服务设计、API文档/契约、接口实现、运行验证和后端交付；不承接原型设计、前端代码或测试执行。用于定义或校验指标数值显示契约。用户提到单位、小数位、百分比、pt改%、比例/比率、raw unit/display unit、scale、rounding、tooltip/export precision、formatter ownership、null/zero/denominator-zero、负零、前后端/API/导出数值不一致时触发；不负责整页设计提升或图表布局。"
---

# Metric Number Display Contract

## Stage Scope

Classification: 后端阶段.

Use this copy only inside the backend/data-service skill bundle. Treat frontend, prototype, and testing work as contracts, evidence, handoff notes, or blockers; do not edit those stages from this skill.

## Positioning

Use this skill when metric-bearing artifacts need stable numeric semantics across requirements, data model, API, backend, frontend, chart/table/KPI display, tooltips, export, testing, and QA.

Use `report-design-system-governance` for full report design-system standards, and use this skill only for number/unit/precision/display contracts.

## Reference Loading

- Read `references/number-precision-display-rules.md` before accepting metric display, formatter, export precision, or percent/rate behavior.

## Anti-Laziness Gate

For non-trivial work, apply `$quality-gate-validation` `references/anti-laziness-execution-gate.md` before final output, handoff, or readiness. Do not mark the result ready while `LAZY-*` findings remain open, when available local evidence was not inspected, when owning skills were skipped, or when proof is limited to generic statements such as "checked", "optimized", "looks good", or "implemented".

## Workflow

1. Identify each metric field and its value type: count, money, rate, ratio, percentage point, duration, score, rank, or derived formula.
2. Define raw value, raw unit, display unit, scale, screen precision, tooltip precision, export precision, rounding mode, and formatter owner.
3. Define null, zero, denominator-zero, negative-zero, missing, and stale-data behavior.
4. Verify consistency across API payload, response metadata, frontend formatter, chart axis/tooltip/table/export, and test expectations.
5. Record breaking changes when type, unit, scale, precision, formula, or nullability changes.

## Required Output

- Metric numeric contract table.
- Formatter ownership and affected surfaces.
- API/backend/frontend/export consistency result.
- Gaps or breaking-change risks.
- Readiness: `ready`, `partial`, or `blocked`.

## Quality Gate

- Do not mark governed report metrics ready when formatting is scattered through `toFixed`, ad hoc `%` concatenation, string slicing, `parseInt`, or component-local decimal assumptions.
- Chinese rate/change labels use `%` unless the domain explicitly requires another convention.
