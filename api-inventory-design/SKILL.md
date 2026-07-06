---
name: api-inventory-design
description: "[后端阶段] 本阶段版本仅服务后端/数据服务设计、API文档/契约、接口实现、运行验证和后端交付；不承接原型设计、前端代码或测试执行。用于在开发前把需求、指标、prototype PRD 执行包、docs/prototype-data-summary.md、mock数据、数据源或前端页面梳理成API清单/接口规划。用户提到接口清单、API清单、接口规划、接口拆分、接口复用、快照接口、snapshotDate/dataVersion/loadBatch、页面需要哪些接口、mock转接口、Mock API To HTTP API Replacement Matrix、Metric To Interface/Source Mapping、响应字段兼容、新增字段命名、请求参数、响应模型、筛选分页排序、筛选前数据完整性、默认后端技术栈、Python/Flask/连接池/Redis、鉴权、接口优先级时触发；只做清单规划，不写完整API文档或后端代码。"
---

# API Inventory Design

## Stage Scope

Classification: 后端阶段.

Use this copy only inside the backend/data-service skill bundle. Treat frontend, prototype, and testing work as contracts, evidence, handoff notes, or blockers; do not edit those stages from this skill.

## Core Positioning

Use this as a reusable artifact skill when the required deliverable is an API清单 rather than full API documentation, backend code, frontend code, or test cases.

The inventory is a planning and alignment artifact. It defines the API surface, model dependency, request scope, response model names, and unresolved questions. It can be used by 技术方案, 数据服务, 前端联调, backend implementation, and testing workflows. Detailed request/response examples belong to downstream API documentation when that deliverable is requested.

## Inputs

- Requirements or page/module descriptions.
- Metric list and dimension/filter definitions.
- Prototype PRD execution bundle and `docs/prototype-data-summary.md`, when the work originates from `report-prd-document-generation` or `report-prototype-implementation-workflow`.
- `Mock API To HTTP API Replacement Matrix` and `Metric To Interface / Source Mapping`, including component data keys, mock endpoints/local datasets, filters, interactions, actions, exports, details, and conclusion-rule inputs.
- 数据模型文件 or source metadata, if available.
- Prototype data code, mock/display data, TypeScript types, data-source registry, or component field usage. If the inventory will feed backend/API implementation with simulated data, plan a SQLite fixture database rather than a JSON data source.
- Existing API notes or backend constraints, if provided.

## Reference Map

Read only the reference files needed for the current task:

| Need | Read |
| --- | --- |
| Produce the exact API清单 table and required columns | `$delivery-artifact-template-management` |
| Decide endpoint boundaries, common endpoint patterns, and when to split or merge APIs | `references/02-endpoint-patterns-and-splitting.md` |
| Define inventory-level request params, response model references, auth, pagination, sorting, filters, exports, and actions | `references/03-request-response-auth-rules.md` |
| Design APIs that make backend implementation simple, efficient, and reusable | `references/05-backend-friendly-api-design.md` |
| Run API traceability, status, no-invention, and gap-linking checks | `references/04-api-stability-gate.md` |
| Required output columns, hard constraints, and final quality gate | `references/06-inventory-output-and-gates.md` |
| Keep interface implementation minimal: filters as params, table-content evidence first, query-only source retrieval | `$backend-development-workflow` `references/minimal-interface-implementation-principles.md` |
| Metric number display contract for response fields | `$metric-number-display-contract` |
| SQL/query feasibility for database-backed APIs | `$sql-query-optimization` |
| Redis/cache/precompute API behavior | `$redis-cache-design-patterns` |
| Environment profile handoff for runtime-bound APIs | `$environment-profile-contract` |
| Resolve authority conflicts and audit whether endpoint boundaries support business question, UI contract, data model, permissions, and tests | `$quality-gate-validation` |

Loading guidance:

- For any generated or updated API清单, load the API inventory template from `$delivery-artifact-template-management` plus the three local references below.
- For a quick endpoint review, read `02-endpoint-patterns-and-splitting.md`, `05-backend-friendly-api-design.md`, and `04-api-stability-gate.md`.
- For export, action, permission, pagination, or dynamic filter APIs, `03-request-response-auth-rules.md` is mandatory.
- Before final delivery, load `06-inventory-output-and-gates.md`.

## Anti-Laziness Gate

For non-trivial work, apply `$quality-gate-validation` `references/anti-laziness-execution-gate.md` before final output, handoff, or readiness. Do not mark the result ready while `LAZY-*` findings remain open, when available local evidence was not inspected, when owning skills were skipped, or when proof is limited to generic statements such as "checked", "optimized", "looks good", or "implemented".

## Targeted Reading Consumption

For PRD/prototype-derived report work, read `prd/execution/prd-targeted-reading-analysis.md` before endpoint inventory. The API清单 must cite consumed `SRC-*` / `READ-*` rows, note non-authority materials, and link open `ENTRY-*` / `GAP-*` rows to endpoint scope, request params, response models, data-version behavior, filters, exports, detail/drilldown, and conclusion-rule inputs. Do not mark inventory rows `ready` when targeted reading is missing, generic, or not traceable to the affected API family.

## Workflow

0. Check source authority.
   When multiple artifacts influence the inventory, identify which source owns business scope, visible UI needs, existing API behavior, source model facts, and testing evidence. If artifacts conflict on endpoint scope, request params, response fields, metric grain, permission, or API availability, record `ENTRY-*` findings instead of silently choosing one.
   For prototype-derived report work, the PRD execution bundle owns report type, page/block/slot/component decisions, interaction behavior, metric definitions, and visible acceptance; `docs/prototype-data-summary.md` owns mock endpoints, local datasets, data keys, and replacement expectations. Do not rebuild API scope from screenshots or final DOM when these files exist.

0a. Apply minimal interface planning.
   For every table-backed or mock-to-real API candidate, inspect or require table-content evidence before interface planning: physical table/view/fixture/upstream object, row grain, keys, filter fields, representative rows, permission fields, result bounds, and gaps. Mark `GAP-*` when the inventory cannot show what each involved table contains.

1. Build page and module coverage.
   List every page, tab, card, chart, table, drawer, export, drilldown, filter option, and action that needs data.
   Include every component data key, slot, filter surface, toolbar action, export, detail/drilldown trigger, and conclusion-rule input named in the prototype data summary or PRD execution files.

2. Identify data access patterns.
   Separate summary KPIs, trends, rankings, lists, analytical tables, detail drawers, filter options, exports, and operational actions. Avoid forcing all data into one endpoint when grain, refresh, filters, or permissions differ.

3. Define endpoint candidates.
   For each API, state method, path, page/module, purpose, trigger, request source, response model, source model dependency, auth need, cache/performance/SLA expectation, priority, and status.
   For each API candidate derived from prototype/mock data, include the replacement-matrix row id, original mock endpoint or local dataset, component data key, consuming slot/component, and whether the endpoint provides metric inputs, filter options, action result, export payload, detail payload, or conclusion-rule inputs.
   Default implementation type for table-backed candidates is `source-query-simple`: one authoritative table/view/fixture/upstream object, explicit projection, request-param predicates, backend-injected permission scope, stable order, bounded pagination, and no hidden joins, aggregation, totals, exact counts, formulas, rankings, or in-memory reshaping.

3a. Assign backend reuse patterns.
   For every production-bound or repeated endpoint, classify the backend implementation family: `metadata`, `filter-options`, `query`, `dashboard/snapshot`, `export`, `action`, or `health/status`. Record which common request model, response envelope, query context, permission service, cache/precompute family, pagination/export flow, or formatter can be reused. Mark `DESIGN-*` when an endpoint would require a one-off controller/query without a clear reason.

4. Define request contracts at inventory level.
   Capture path/query/body params, filters, period format, organization scope, pagination, sorting, keyword search, drilldown params, export params, and default values. Separate client-supplied params from backend-defaulted params and backend-injected permission/data-scope params.
   Every client-visible filter that changes returned rows must be a request param with source field, operator, allowed/default value, and invalid-param behavior. Do not hide filters as UI-only state, controller defaults, previous endpoint state, or application memory.

5. Define data-version and endpoint dependency contracts.
   When a report has snapshot/latest-period semantics, first classify the snapshot role: overview-only payload, canonical/shared snapshot dataset, reusable response for a bounded component group, or local/demo artifact. State which endpoint or metadata source exposes `snapshotDate`, `latestPeriod`, `loadBatch`, `dataVersion`, or equivalent fields, and require every related snapshot, metrics, trend, ranking, table, export, and health API to consume the applicable data-version and scope values as backend query context or to explicitly reuse the declared snapshot dataset. Define whether each value is client-supplied, backend-defaulted, or backend-injected from auth/permission. Do not leave metrics/trend/table dependency on `/snapshot`, controller-level memory, or previous frontend call order implicit. Each data-bearing API must either filter its own source/logical model, repository query, precompute table, or Redis key with the shared version context and correct business/permission scope, or document that it derives from the canonical snapshot and why the grain/scope/version match.

6. Define filter data support at inventory level.
   Before marking filter-bearing APIs ready for downstream implementation, capture option source, source/provider execution stage, required fields, row grain, default state, non-default state, empty/no-permission state when relevant, and resolver/API branch need. Record a `GAP-*` when the planned API can only produce one default snapshot for an affecting filter.

6a. Define aggregation/processing exceptions.
   If the consuming page needs aggregate, ranking, total, formula, chart-series, or summary-card data, first check whether an existing source table already stores that grain. If yes, model the API as a simple query against that source-aligned table. If no, mark a derived/summary/precompute `GAP-*` or route to data-model/precompute design; do not make a simple interface inventory row imply hidden aggregation.

7. Define response contracts at inventory level.
   Reference a response model name and summarize required field groups, grain, list/envelope shape, empty state, and error behavior. Do not duplicate the full API document here.
   For metric-bearing fields, use `$metric-number-display-contract` to record value type, unit, scale, precision, percent/rate behavior, rounding, and formatter owner at inventory level.

7a. Define response compatibility for source replacement.
   If an API may move from mock/SQLite to real source, or from one table/upstream to another, record that existing response field codes and behavior remain stable and that source-field changes are handled by the model/adapter layer. Additive fields must be named by convention and linked to source/model. Required renames, removals, type/unit/precision/enum/nullability/formula/grain changes, or empty/no-permission behavior changes are breaking and need versioning plus impact analysis.

8. Mark gaps.
   If an endpoint depends on unknown data models, formulas, enums, filter options, permission rules, or owner decisions, record the gap in the pending column with a stable `GAP-*` ID, impact, owner question, and blocking status.
   Missing replacement rows, unmapped component data keys, unowned conclusion inputs, and prototype summary files that are absent or stale are blocking gaps for prototype-derived backend inventories.

9. Run the design reasonableness gate.
   Check whether endpoint boundaries, split/merge choices, response model references, request params, dynamic options, exports, actions, auth, and performance notes reasonably support the consuming page and tests. Record unreasonable API inventory choices as `DESIGN-*` findings.
   For database-backed APIs, call `$sql-query-optimization` when query shape, sort/page/count, or index feasibility is risky. For Redis/cache APIs, call `$redis-cache-design-patterns`.
