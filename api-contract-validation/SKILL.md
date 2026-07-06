---
name: api-contract-validation
description: "[后端阶段] 本阶段版本仅服务后端/数据服务设计、API文档/契约、接口实现、运行验证和后端交付；不承接原型设计、前端代码或测试执行。用于校验 API 契约是否与文档、前端期望、后端路由、mock、OpenAPI、数据库/上游样例、运行响应一致。用户提到接口契约校验、前后端字段不一致、响应字段缺失、类型/单位/枚举/精度错误、百分比/比例值口径、响应字段变化、新增字段命名、请求参数、分页排序筛选、筛选前数据完整性、snapshotDate/dataVersion/loadBatch、快照接口依赖、空态错误态、鉴权头、mock替换前验证、联调问题定位时触发。"
---

# API Contract Validation

## Stage Scope

Classification: 后端阶段.

Use this copy only inside the backend/data-service skill bundle. Treat frontend, prototype, and testing work as contracts, evidence, handoff notes, or blockers; do not edit those stages from this skill.

## Positioning

Use this skill to compare API contracts across producer and consumer evidence. It is side-neutral: apply it before backend implementation, before frontend mock replacement, after route changes, or during integration debugging.

It validates behavior and records differences. It does not design a new API inventory, write full API documentation, or implement backend/frontend code unless another workflow asks for that.

## Reference Loading

- Backend/source authority and runtime validation: `references/backend-contract-sources-and-authority.md`, `references/backend-response-and-request-validation.md`, `references/backend-runtime-source-validation.md`
- Backend validation note: `references/backend-validation-note-template.md`
- Frontend provider evidence and comparison checklist: `references/frontend-source-contract-types.md`, `references/frontend-comparison-checklist.md`
- Frontend contract note: `references/frontend-contract-note-template.md`
- Numeric unit/precision/percentage/display consistency: `$metric-number-display-contract`
- Cross-artifact conflicts or readiness gates: use `$quality-gate-validation`.

## Anti-Laziness Gate

For non-trivial work, apply `$quality-gate-validation` `references/anti-laziness-execution-gate.md` before final output, handoff, or readiness. Do not mark the result ready while `LAZY-*` findings remain open, when available local evidence was not inspected, when owning skills were skipped, or when proof is limited to generic statements such as "checked", "optimized", "looks good", or "implemented".

## Workflow

1. List all contract evidence: API docs, OpenAPI, route code, frontend clients, mock data, provider samples, DB/upstream samples, runtime responses, env/auth notes, and test failures.
2. Decide authority order. If sources conflict on behavior, run `$quality-gate-validation` before changing affected contracts.
3. Compare request contract: method/path, params, filters, pagination, sorting, headers, auth, defaults, invalid values, and permission scope.
4. Compare minimal interface implementation evidence when the API is table-backed or mock-to-real.
   Verify every involved table/view/fixture/upstream object has table-content evidence: source object, row grain, keys, filter fields, representative samples, permission fields, result bounds, and gaps. Verify every client-visible filter is a request param mapped to a source/provider predicate. Verify simple retrieval endpoints are query-only and do not add hidden joins, aggregation, exact counts, totals, rankings, formulas, chart/KPI derivation, or broad in-memory reshaping.
5. Compare filter data completeness before binding readiness.
   For every filter/search/sort/page param that should change business data, verify option data, matching source/provider rows, required response fields, default sample, at least one non-default sample, empty/no-permission sample when relevant, and resolver/API branch coverage. If this evidence is missing, classify the contract as data-completeness or data-grain `missing/blocked` before judging frontend binding.
6. Compare data-version, snapshot role, and endpoint dependency contract.
   For snapshot/latest-period API groups, verify `snapshotDate`, `latestPeriod`, `loadBatch`, `dataVersion`, report version, or source version is exposed/defaulted consistently and included in request/query/cache context where needed. Verify business filters and permission/data scope are applied as backend params, source/provider predicates, precompute lookup keys, declared snapshot reuse rules, or Redis/cache key segments before response construction. Confirm metrics, trends, rankings, tables, drilldowns, and exports either validly reuse a declared canonical/shared snapshot or avoid dependency on undocumented snapshot responses, frontend call order, or controller-memory snapshots.
7. Compare response contract: envelope, fields, nesting, types, units, precision, numeric display contract, enum values, dates, totals, empty states, errors, and no-permission states. For metric-bearing fields, use `$metric-number-display-contract`. For rate/percentage fields, identify whether the API returns a raw ratio (`0.744`), percent number (`74.4`), or display-ready string (`74.4%`), and record display owner and rounding rules.
   For every metric-bearing field, validate value type, raw/display unit, display scale, screen precision, tooltip/export precision, rounding mode, null/zero/denominator-zero behavior, negative-zero handling, small-nonzero behavior when relevant, formula precision policy, and formatter ownership across docs, mocks, route/runtime samples, source samples, frontend adapters, and exports.
7a. When a backend source table/upstream/fixture has changed, compare old and new runtime or fixture responses against the same API contract. Existing fields must remain present and behavior-compatible; newly added fields must be additive, conventionally named, documented, and safe for consumers to ignore.
8. Compare runtime/source behavior when available: mock vs fixture vs DB/upstream vs live API.
9. Classify each finding as pass, mismatch, missing, ambiguous, blocked, or not tested.

## Required Output

- Contract evidence inventory and authority decision.
- Field/request/state comparison matrix.
- Minimal interface evidence result: table-content evidence, request-param-to-source-field mapping, query-only proof, hidden-processing findings, and derived/summary exceptions.
- Numeric display/precision comparison matrix for metric-bearing fields.
- Source/table replacement compatibility result when applicable: preserved fields, changed fields, additive fields, missing mapping, and version/deprecation need.
- Filter data-completeness result before binding readiness.
- Parameter-driven data-version, snapshot role/reuse, scope-filtering, and endpoint-dependency result when snapshot/latest-period semantics exist.
- Findings with severity, expected, actual, evidence, owner side, and suggested repair.
- Readiness: `ready`, `partial`, or `blocked`.
- Handoff notes for API docs, backend, frontend, or testing.

## Quality Gate

- Do not mark pass when required evidence is absent.
- Do not silently merge contradictory API docs, mocks, route code, and runtime samples.
- Every mismatch includes field/path/state, expected value, actual value, and evidence source.
- Source/table replacement validation is not ready when existing response fields are renamed, removed, moved, type-shifted, unit/precision/enum/nullable-shifted, formula-shifted, or grain-shifted without an approved versioned breaking change and downstream migration plan.
- New response fields are not ready when naming, source trace, type, unit, nullability, permission/sensitivity, or additive compatibility status is missing.
- Table-backed APIs are not ready when table content, row grain, keys, filter fields, representative samples, result bounds, or permission fields were not inspected.
- Client-visible filters are not ready when they are hidden as UI state, code defaults, previous endpoint state, controller memory, or any mechanism other than request params mapped to source predicates.
- Simple retrieval APIs are not ready when runtime/code/docs show hidden joins, aggregation, exact counts, totals, rankings, formulas, chart/KPI derivation, or broad in-memory processing without an approved derived/summary/precompute contract.
- Frontend-facing readiness includes loading, empty, error, auth, no-permission, and partial data states.
- Frontend-facing rate/change/completion contracts are not ready until raw value scale, display scale/unit, rounding, and owner are explicit. Visible Chinese report labels should use `%` unless the contract explicitly and intentionally requires `pt`, `p.p.`, or `percentage point`.
- Metric-bearing contracts are not ready when KPI/chart/table/tooltip/drawer/export use inconsistent units, scales, decimals, rounding, null/zero/denominator-zero handling, or when numeric logic depends on rounded display strings instead of raw numeric values and numerator/denominator recomputation.
- Filter/search/sort/page params are not ready until data completeness is proven before binding: option values, source/provider rows, required fields, default/non-default runtime or fixture samples, and resolver/API branches exist or are marked blocked.
- Filter/search/sort/page params are not ready when the contract only changes UI selected state or omits the provider/resolver fields needed to rebuild the response for non-default states.
- Snapshot/latest-period API groups are not ready when shared data-version fields are missing, snapshot reuse is undocumented, or one data-bearing endpoint consumes another endpoint's runtime payload instead of a declared snapshot/source/logical/precompute/cache contract.
- Data-bearing APIs are not ready when changing `snapshotDate/dataVersion/loadBatch`, business filters, or permission/data scope does not change the backend query/cache key or verified result scope as expected.
