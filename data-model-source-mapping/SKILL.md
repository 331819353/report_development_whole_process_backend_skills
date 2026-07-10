---
name: data-model-source-mapping
description: "[后端阶段] 本阶段版本仅服务后端/数据服务设计、API文档/契约、接口实现、运行验证和后端交付；不承接原型设计、前端代码或测试执行。用于创建或修正数据模型文件和数据源到消费端映射。用户提到数据模型、字段模型、数据源映射、源表、元数据、逻辑模型、响应模型、视图模型、更换数据源/数据表、API返回字段保持不变、新增字段规范命名、指标/字段口径、维度关系、snapshotDate/dataVersion/loadBatch、数据版本、筛选前数据完整性、筛选数据粒度、原型mock字段、数据血缘、刷新频率、权限、质量规则时触发；不负责API文档或代码实现。"
---

# Data Model Source Mapping

## Stage Scope

Classification: 后端阶段.

Use this copy only inside the backend/data-service skill bundle. Treat frontend, prototype, and testing work as contracts, evidence, handoff notes, or blockers; do not edit those stages from this skill.

## Core Positioning

Use this as a reusable artifact skill when the deliverable is a 数据模型文件 or source-to-consumer mapping that connects requirements, APIs, frontend contracts, tests, or real data sources.

This skill is not limited to the 技术方案 stage. In 技术方案 it defines the model handoff; in 数据服务 it supports API documentation and transformation design; in 前端联调 it explains how response fields map to UI expectations; in 测试校验 it provides the traceability basis for data consistency checks.

The model file must explain not only field names, but also source ownership, grain, refresh cadence, relationships, metric formulas, transformations, permissions, and what each model supports.

## Inputs

- Data-source documents with tables, views, files, APIs, fields, metadata, owner, permission, and refresh rules.
- Requirements and metric lists.
- Prototype data code, mock data, TypeScript interfaces, component data fields, filters, and response-like structures.
- API清单 or endpoint draft, if available.

## Reference Map

Read only the reference files needed for the current task:

| Need | Read |
| --- | --- |
| Produce the exact 数据模型文件 structure and required table columns | `$delivery-artifact-template-management` |
| Map physical sources into logical models and response/view models | `references/02-source-logical-response-mapping.md` |
| Define metric formulas, transformations, permissions, and data-quality rules | `references/03-metrics-transformations-quality.md` |
| Run model traceability, no-invention, and pending-item routing checks | `references/04-model-stability-gate.md` |
| Required model output, hard constraints, and final quality gate | `references/05-model-output-and-gates.md` |
| Minimal interface implementation source evidence: table content first, filters as params, query-only retrieval | `$backend-development-workflow` `references/minimal-interface-implementation-principles.md` |
| Metric number display contract for logical/response fields | `$metric-number-display-contract` |
| Resolve authority conflicts when requirements, metric lists, prototype code, API contracts, source documents, or tests disagree | `$quality-gate-validation` |
| Audit whether source/logical/response model design reasonably supports the business question, API inventory, frontend contract, permissions, and tests | `$quality-gate-validation` |

Loading guidance:

- For any generated or updated 数据模型文件, load the data model template from `$delivery-artifact-template-management` plus the three local references below.
- For source-to-response mapping only, use `$delivery-artifact-template-management`, `02-source-logical-response-mapping.md`, and `04-model-stability-gate.md`.
- For metric-heavy work, `03-metrics-transformations-quality.md` is mandatory.
- Before final delivery, load `05-model-output-and-gates.md`.

## Anti-Laziness Gate

For non-trivial work, apply `$quality-gate-validation` `references/anti-laziness-execution-gate.md` before final output, handoff, or readiness. Do not mark the result ready while `LAZY-*` findings remain open, when available local evidence was not inspected, when owning skills were skipped, or when proof is limited to generic statements such as "checked", "optimized", "looks good", or "implemented".

## Targeted Reading Consumption

For PRD/prototype-derived report mapping, read `prd/execution/prd-targeted-reading-analysis.md` before source/model decisions. The model file must cite consumed `SRC-*` / `READ-*` rows, identify authoritative vs non-authoritative source materials, and link `ENTRY-*` / `GAP-*` to source tables, grains, metric formulas, response fields, data-version fields, filter completeness, permission scope, and quality rules. Do not mark source/model rows `ready` when targeted reading is missing, generic, or not reflected in lineage.

For completed-prototype handoff, also load `backend-development-workflow/references/00-prototype-downstream-handoff-contract.md`. Preserve accepted `MET-*`, `OBJ-*`, `DATA-DESIGN-*`, `API-*`, `FILTER-*`, `INT-*`, and `RULE-*` IDs through source/logical/response mappings and link every physical source to `tableContentUnderstandingMatrix` evidence.

## Workflow

0. Check source authority.
   When multiple artifacts define the model, identify which source owns physical fields, metric formula, grain, response/view needs, permission, freshness, and sample evidence. If they conflict on source field, join, formula, enum, grain, permission, or response shape, record `ENTRY-*` findings before creating a model assumption.

1. Identify source systems.
   List every source table/view/file/API, owner, business domain, refresh cadence, access method, permission need, expected volume, and known quality issue.

2. Understand each source table's data content before mapping.
   For every table/view/fixture/upstream object, inspect or require schema, row grain, keys, partition/date fields, filter fields, permission fields, representative sample rows, nullable/enumerated fields, measure-like columns, result bounds, and gaps. Do not design a response model, join, aggregation, or metric formula from a table name alone.

3. Define source models.
   For each source, capture physical name, business meaning, grain, primary key, natural keys, partition/date fields, dimensions, measures, enums, nullable fields, and sample values.

4. Define logical/business models.
   Combine sources into business objects such as customer, order, project, inventory, contract, payment, task, alert, organization, or period. Define joins, relationship cardinality, aggregation grain, and ownership.

5. Define response/view models.
   Map prototype/API-facing fields to logical/source fields. Include display labels, field types, units, precision, numeric display contracts, enum labels, sorting, empty-state behavior, and whether the field is calculated.
   Use `$metric-number-display-contract` for value type, raw/display unit, display scale, precision, percent/rate behavior, tooltip/export precision, rounding, null/zero/denominator-zero behavior, and formatter owner.

5a. Preserve response contract compatibility during source replacement.
   When the source table, upstream API, fixture schema, or serving model changes, keep existing response/view field codes and behavior stable. Produce a before/after mapping: response field -> old source field/formula -> new source field/formula -> transformation/default/null rule -> verification evidence. New response fields must be additive and named by the project convention; if absent, use stable English lowerCamel field codes. Any required rename, type/unit/precision/enum/nullability/formula/grain change is a breaking `DESIGN-*` or `GAP-*` item until versioning and downstream impact are explicit.

6. Define data-version and snapshot semantics.
   When the report needs current/latest/snapshot behavior, document the snapshot role, business time field, `snapshotDate` or `latestPeriod`, `loadBatch`, `dataVersion`, source partition, report version, freshness timestamp, and invalidation/backfill rule. Clarify which response models expose version metadata, which fact/logical/precompute/snapshot models are queried or reused by each endpoint, and which source fields or partitions those params filter. If an API response is intentionally the canonical/shared snapshot for other components, model it as a named snapshot/precompute/view model with grain, fields, scope, and reuse rules instead of treating it as an incidental response.

7. Define filter-supporting data completeness.
   When consuming pages or APIs have filters, document the filter option source, request param name, source predicate field, fact/business row grain, required fields, default state, at least one non-default state, empty/no-permission state when relevant, and resolver/API branch dependency before declaring the response/view model filter-ready. Single default snapshots are not enough for affecting filters unless the component is explicitly invariant.

8. Define metric formulas.
   For each metric, document formula, numerator, denominator, filter scope, period logic, baseline, threshold, direction, unit, precision, numeric display contract, and reconciliation rule.

9. Define transformation notes.
   For simple interface implementation, keep transformations to source aliases, type serialization, masking, and null preservation. Capture date conversion, period aggregation, unit conversion, enum mapping, rounding, default fill, hierarchy rollup, deduplication, and permission filtering only when the contract explicitly needs them; aggregation/derived work requires a named source table, precompute, or `GAP-*`.

10. Mark gaps.
   Record unresolved source, field, formula, enum, join, sample, owner, refresh, or permission gaps in this skill's pending model items with stable `GAP-*` IDs, impact, owner question, current assumption, and downstream blocking status.

11. Run the design reasonableness gate.
   Check whether the model grain, joins, response/view models, metric formulas, transformation strategy, permissions, freshness, and quality rules reasonably support the consuming APIs, UI components, filters, and tests. Record unreasonable model structures as `DESIGN-*` findings.
