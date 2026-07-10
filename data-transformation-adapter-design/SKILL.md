---
name: data-transformation-adapter-design
description: "[后端阶段] 本阶段版本仅服务后端/数据服务设计、API文档/契约、接口实现、运行验证和后端交付；不承接原型设计、前端代码或测试执行。用于设计和校验数据从源头到消费端的转换与适配逻辑。用户提到字段映射、源表到响应、上游到API、mock到数据库、响应字段兼容、新增字段命名、response adapter、响应适配、snapshotDate/dataVersion/loadBatch、筛选前数据完整性、筛选数据粒度、嵌套拉平、枚举翻译、单位/精度/日期转换、百分比/比例显示、汇总聚合、公式派生、null默认值、组件view model、前后端结构不一致时触发。"
---

# Data Transformation Adapter Design

## Stage Scope

Classification: 后端阶段.

Use this copy only inside the backend/data-service skill bundle. Treat frontend, prototype, and testing work as contracts, evidence, handoff notes, or blockers; do not edit those stages from this skill.

## Positioning

Use this skill when source data, API response data, and UI view models do not naturally match. It covers both backend transformation and frontend response adapters, while keeping their boundaries explicit.

Backend transformation owns source-to-API correctness. Frontend adapter owns provider-payload-to-UI-model stability.

For backend interface implementation, adapters are not a license to add hidden business logic. The default path is source-query-simple: understand the source table content, expose filters as request params, query rows only, and use adapters only for stable aliases, serialization, masking, null handling, and compatibility. Aggregation, formulas, totals, rankings, and broad reshaping require an explicit derived/summary/precompute contract or `GAP-*`.

## Reference Loading

- Backend boundary, source-to-target mapping, required/default fields: `references/backend-boundary-and-mapping.md`
- Time conversion, aggregation, formula, ranking, totals, reconciliation: `references/backend-time-aggregation-derivation.md`
- Backend implementation and verification notes: `references/backend-implementation-and-verification.md`
- Frontend adapter placement: `references/frontend-adapter-placement-patterns.md`
- Frontend mapping resilience: `references/frontend-mapping-resilience-rules.md`
- Adapter output template: `references/frontend-adapter-output-template.md`
- Numeric unit/precision/percentage/display contract: `$metric-number-display-contract`

## Anti-Laziness Gate

For non-trivial work, apply `$quality-gate-validation` `references/anti-laziness-execution-gate.md` before final output, handoff, or readiness. Do not mark the result ready while `LAZY-*` findings remain open, when available local evidence was not inspected, when owning skills were skipped, or when proof is limited to generic statements such as "checked", "optimized", "looks good", or "implemented".

## Targeted Reading Consumption

For PRD/prototype-derived report adapters, read `prd/execution/prd-targeted-reading-analysis.md` before transformation rules. The adapter design must cite consumed `SRC-*` / `READ-*` rows, non-authority notes, and open `ENTRY-*` / `GAP-*` rows that affect source-to-response mapping, response-to-view-model mapping, numeric semantics, null/default behavior, retained mocks, and compatibility decisions. Do not mark an adapter `ready` when targeted reading is missing, generic, or not reflected in field-level mappings.

For completed-prototype handoff, also load `backend-development-workflow/references/00-prototype-downstream-handoff-contract.md`. Adapters may preserve explicit field/serializer compatibility but must not hide missing request filters, business aggregation, formulas, totals, rankings, broad reshaping, or UI layout semantics.

## Workflow

1. Identify source payload, target API contract, and UI/view model contract.
2. Inspect table/content evidence before adapter design: source object, row grain, keys, request filter fields, permission fields, sample rows, result bounds, and gaps.
3. Define grain, required fields, optional fields, defaults, null behavior, precision, units, numeric display contract, enum dictionaries, date/time formats, and locale labels.
4. For metric-bearing fields, apply `$metric-number-display-contract`: keep raw numeric value, calculation value, display unit, display scale, screen precision, tooltip/export precision, rounding mode, null/zero/denominator-zero behavior, negative-zero handling, and formatter owner explicit. For rate/percentage/change fields, keep calculation value, display value, display unit, rounding, and label wording explicit. Chinese report UI display values should render `%` for rates unless the user or contract intentionally requires another term.
5. Decide execution boundary: SQL/source query, backend service/DTO, API gateway/BFF, frontend adapter, or component-local display formatting. For simple table retrieval, keep the backend boundary at projection, predicates, stable order, pagination, and serializer aliases only.
5a. When the backend source table/upstream/fixture changes, freeze the target API contract first. Map every existing response field from old source to new source and keep field name, nesting, type, unit, precision, enum meaning, nullability, formula, grain, and empty/no-permission behavior stable. Put new source names behind adapter rules; expose new fields only as additive fields named by convention and documented with compatibility status.
6. Verify filter data support before adapter binding.
   For every filter that should affect the transformed output, define option source, input param, source/provider field, row grain, required fields, default example, non-default example, empty/no-permission example when relevant, and resolver/API branch behavior. If the source only has one default snapshot, classify it as a data-completeness gap before designing UI binding or adapter-side filtering.
7. Verify data-version and endpoint-source boundaries.
   For snapshot/latest-period APIs, keep `snapshotDate`, `latestPeriod`, `loadBatch`, `dataVersion`, report version, or source version as query metadata/context that can flow across requests and must map to backend source predicates, precompute lookups, snapshot reuse rules, or cache keys. One endpoint's business payload may feed another component or response only when the API/model contract declares it as a canonical/shared snapshot or bounded component-group payload with matching grain, fields, filters, permission scope, version params, cache key, and invalidation behavior.
8. Specify transformations. For source-query-simple APIs, restrict transformations to rename/alias, mask, type serialization, null behavior, and permission metadata. Group, aggregate, derive, rank, total, reconcile, or broad reshape work must be marked as an approved derived/summary exception or `GAP-*`.
9. Provide representative before/after examples and edge cases.
10. Define verification cases for default, filtered, empty, abnormal, missing, permission-limited, and large-result states.

## Required Output

- Source contract, target contract, and owner boundary.
- Table/content understanding evidence before adapter rules: source object, grain, keys, filter fields, samples, permission fields, bounds, and gaps.
- Field mapping table with formulas, units, precision, enums, defaults, and required status.
- Minimal interface boundary proof: request filters as params, query-only retrieval, and no hidden aggregation/processing unless an exception is named.
- Numeric display/precision contract for metric-bearing fields, including percent scale and formatter owner.
- Source replacement compatibility table when applicable: existing target field, old source, new source, transform/default/null rule, unchanged behavior evidence, additive fields, and blocked breaking changes.
- Transformation/adaptation rules and examples.
- Filter data support proof before binding: option source, row grain, default/non-default examples, fields, and resolver/API branch coverage.
- Data-version metadata, backend query binding, and endpoint-source boundary when snapshot/latest-period APIs exist.
- Verification cases and unresolved gaps.
- Readiness: `ready`, `partial`, or `blocked`.

## Quality Gate

- Do not hide business aggregation, global filtering, pagination, or permission scope inside a frontend adapter unless explicitly bounded.
- Do not use backend adapters to hide missing request params, missing table-content evidence, joins, aggregation, totals, rankings, formulas, or broad response reshaping for a simple interface.
- Do not let backend publish fields whose source, formula, enum, or unit is unknown.
- Do not let a source/table/upstream replacement rename or reshape existing API response fields. Compatibility repair belongs in mapping/adapter logic; unavoidable response drift requires explicit API versioning, deprecation, and impact analysis.
- Do not expose new response fields from new source columns until they follow the project naming convention, are additive, and have source/type/unit/nullability/permission documentation.
- Adapter output must keep component view models stable or document the exact refactor.
- Examples must prove the transformation for at least one non-default case when filters or formulas matter.
- Do not claim a filter-aware adapter is ready until data completeness is proven first; missing non-default rows, fields, option data, or resolver/API branches are data gaps.
- Do not collapse raw numeric values and formatted display strings into one ambiguous field when downstream calculations, sorting, tooltips, exports, or tests need the original value.
- Do not use adapters to round before aggregation, totals, ranking, threshold comparison, or reconciliation; formatting happens at the display/export edge unless metric governance explicitly says otherwise.
- Do not use a frontend adapter to fake filter variation over one default snapshot; add provider/resolver branches, query params, or row grain that proves non-default states.
- Do not use an adapter to make metrics/trend/table/export data from an undocumented snapshot API payload when the API contract requires independent backend/source data. Declared canonical/shared snapshot reuse is valid; accidental payload reuse is not.
- Do not use response transformation to hide missing backend filtering. If version, business filter, or permission scope affects correctness, it must be applied by the backend source/precompute/cache query before adapter formatting.
