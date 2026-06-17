# Report Delivery Pipeline Contract

Use this shared contract from every top-level workflow. It keeps the report delivery pipeline consistent across prototype design, technical solution, backend/data service, frontend integration, and testing.

Every stage artifact must follow the artifact readability gate in `$quality-gate-validation`: produce one dual-readable artifact by default, with human-first summary and narrative plus structured contract tables/appendices for downstream AI extraction. Create separate human and machine outputs only when explicitly requested or when a formal/external/machine-schema deliverable would otherwise make one document hard to review.

Before a top-level workflow builds, repairs, documents, or hands off artifacts from mixed entry materials, run the entry consistency gate in `$quality-gate-validation`. User requirements, HTML/source samples, screenshots, API docs, data models, mock data, frontend/backend code, env/auth notes, and runtime traces may contradict each other; unresolved `P0` and `P1` entry conflicts keep the affected scope `partial` or `blocked` and require user confirmation only before the affected repair or implementation proceeds.

Before a workflow finalizes design, API/model contracts, frontend/backend wiring, visual repair, test cases, or handoff readiness, run the design reasonableness gate in `$quality-gate-validation` when design decisions are in scope. A design can be input-consistent but still unreasonable if it fails the business question, report type, component necessity, data/API feasibility, interaction closure, layout, or testability checks.

Before a workflow marks technical architecture, data service/backend, frontend integration, or testing acceptance as production-ready, run the production closed-loop readiness gate in `$quality-gate-validation`. A stage can be document-complete or locally runnable while still only `partial` if source authority, environment, auth, deployment, observability, performance, testability, or defect retest closure is missing.

Whenever data service or data visualization runtime behavior depends on environment configuration, apply the environment profile gate in `$quality-gate-validation`. Test and production profiles must be represented by `.env.test` and `.env.production`; a single undifferentiated `.env` is not enough for integration, handoff, or production acceptance.

Whenever a report/BI/dashboard frontend visualization is designed, implemented, integrated, validated, or marked production-ready, apply `$frontend-development-workflow`. Visualization decisions such as user purpose, first-screen conclusion, chart/table choice, metric formatting and口径, filters/linkage/drill-through, component-ready provider mapping, loading/empty/error/no-permission states, freshness/quality display, frontend performance, theme/accessibility, and runtime QA evidence must be explicit or intentionally out of scope.

Whenever a report/BI/dashboard data chain, frontend/backend pair, export, permission path, cache path, or release candidate is integration-tested, apply `$testing-integration-workflow`. Testing decisions such as metric口径, golden/baseline data, model reconciliation, API contract, frontend binding, filters, permissions, cache isolation, export parity, performance/stability, exception states, UAT, release smoke, monitoring, rollback, regression, and retest closure must be explicit or intentionally out of scope.

Whenever a data service/API is designed, documented, implemented, validated, or marked production-ready, apply `$performance-optimization`. Performance and stability decisions such as concurrency model, cache, connection pools, timeouts, retries, rate limits, degradation, health checks, and observability must be explicit or intentionally out of scope.

Whenever a report/BI/dashboard backend data service is designed, documented, implemented, validated, or marked production-ready, apply `$backend-development-workflow`. Report query-service decisions such as metadata, permission injection, parameter guardrails, query planning, safe SQL/source generation, component-ready result shape, pagination/count, async export, freshness/quality, audit, cache safety, version/publish/rollback, and slow-report governance must be explicit or intentionally out of scope.

Whenever a database-backed data service/API is designed, documented, implemented, validated, or marked production-ready, apply `$performance-optimization`. Query shape decisions such as projection, predicate sargability, join cardinality, dedup/order necessity, pagination strategy, aggregation/window placement, dynamic optional filters, and plan evidence must be explicit or intentionally out of scope.

Whenever a report/BI/dashboard data model, metric model, source-to-consumer mapping, or OLAP serving model is designed, documented, implemented, validated, or marked production-ready, apply `$performance-optimization`. Modeling decisions such as business question, subject area, business process, grain, fact/dimension type, metric additivity, time口径, DWD/DIM/DWS/ADS layer, summary/wide-table justification, SCD/history, many-to-many handling, deduplication, late-arriving data, quality rules, and lineage must be explicit or intentionally out of scope.

When a request changes an existing delivered or in-progress artifact, route first through `$change-impact-analysis`. Do not patch one document or code surface while leaving affected metrics, API contracts, data models, frontend bindings, tests, permissions, screenshots, or delivery versions unknown.

When backend implementation replaces a data source, source table/view, upstream API, SQLite fixture, precompute table, or serving model, preserve the API response model as the downstream contract. Existing response fields must remain stable in name, nesting, type, unit, precision, enum meaning, nullability, formula, grain, and empty/no-permission behavior. New fields must be additive, named by convention, source-traced, and contract-validated. Any unavoidable drift is a breaking API/model change that needs versioning, deprecation/migration notes, change-impact analysis, and regression scope before the affected artifact can be `ready`.

When artifacts span more than one iteration, maintain a delivery version chain through `$delivery-version-management`. Every prototype/API/model/backend/frontend/test/release artifact should state which upstream version it consumes and which downstream version validated it.

When frontend, backend, or runnable prototype source code is created, repaired, refactored, or modified, maintain file-level code change ledgers through `$code-change-ledger-management`. Every changed scoped code file must have a sidecar ledger under `__change_logs__`, must be read before editing, and must receive a post-change version entry with feature list, changed code ranges/stable anchors, affected contracts, verification, and rollback notes.

## Stage Routing Matrix

All expected user inputs are Chinese. Use this matrix before choosing a workflow:

| 中文意图/触发词 | Workflow | Required Inputs | Primary Outputs | Do Not Use For |
| --- | --- | --- | --- | --- |
| 自助分析、分析工作台、BI自助、拖拽维度指标、自由组合筛选、图表切换、保存个人报表 | `$report-self-service-analysis-prototype-workflow` | Dataset scope, field list, metric/dimension rules, permissions, expected operations | Self-service analysis prototype, field/config/result binding, save/share/export behavior | Fixed dashboard/report-only prototype |
| 指标看板、经营看板、驾驶舱、核心KPI、目标达成、同比环比、趋势排名、异常提醒、预警 | `$report-kpi-dashboard-prototype-workflow` | KPI list, targets, thresholds, update frequency, drilldown needs | KPI dashboard prototype, monitoring hierarchy, anomaly/drilldown behavior | Free exploration or detailed reconciliation |
| 分析报告、专题分析、经营分析报告、复盘、原因归因、结论先行、证据链、行动建议 | `$report-analysis-report-prototype-workflow` | Report question, period/scope, comparison baseline, evidence data, action owner hints | Analysis report prototype, narrative chain, attribution, recommendations | High-frequency monitoring or row lookup only |
| 明细报表、台账、流水、记录查询、筛选排序分页、导出、核对、追溯具体记录 | `$report-detail-report-prototype-workflow` | Row grain, primary key, fields, filters, export scope, source trace target | Detail report prototype, table/query/export/traceability behavior | KPI dashboard or narrative analysis |
| 原型、页面原型、报表原型、仪表盘原型、大屏原型、demo、样机、截图/源码还原、可运行URL，且不明确属于上述四类专项原型 | `$report-design-workflow` | Business purpose, target user, source materials, expected page type, mock/source data if available | Runnable prototype, component mapping, visual/runtime evidence, design handoff | Backend implementation, formal API contract, final UAT |
| 技术方案、技术架构、架构设计、技术选型、实现路径、实施方案、接口规划、数据建模、数据模型、数据源映射、指标字典、权限矩阵、非功能、上线准备、更换数据源/数据表规划 | `$technical-solution-workflow` | Requirement/prototype, source/API hints, metric list, permission expectations, existing stack/env constraints when available | Architecture blueprint, technology selection/ADR, implementation roadmap, API inventory, model/mapping, runtime/security/production readiness, gap/risk ledger | UI polishing, runtime frontend QA |
| 后端、服务端、数据服务、数据服务设计、API服务设计、后端方案、接口实现、接口开发、Flask、启动后端、本地后端、鉴权中间件、更换数据源/数据表实现 | `$backend-development-workflow` | Technical solution/API inventory, data model, data source, auth/env rules, expected runtime target | Data-service design, API docs, backend/API implementation when requested, query-service chain, runtime/security/observability plan, smoke/contract evidence, missing info | Frontend layout or visual QA |
| 前端、页面开发、报表页面、可视化开发、替换mock、接真实接口、接口对接、环境变量、build/preview | `$frontend-development-workflow` | Prototype/source code, API docs/base URL, env/auth details, expected page behavior | Frontend integration, runtime URL/build, QA evidence, function description | Backend contract design |
| 测试、联调测试、集成测试、验收测试、测试用例、冒烟测试、缺陷报告、回归证据 | `$testing-integration-workflow` | Frontend/backend URLs, accounts, API docs, expected data, acceptance scope | Test matrix, execution evidence, defects, retest closure | New feature implementation unless fixing defects is requested |
| 需求变更、变更影响、改已有原型/接口/模型/前端/测试 | `$change-impact-analysis` | Existing artifact/version, change request, target stage | Impact matrix, affected artifacts, safe execution order | Fresh greenfield design |
| 指标字典、指标口径、血缘、计算公式、口径冲突 | `$metric-governance-lineage` | Metric list, formulas, dimensions, source fields | Governed metric dictionary, lineage, conflict log | Runtime UI QA |
| 交付版本、版本链路、阶段交接、发布包、验收包 | `$delivery-version-management` | Artifact list, stage outputs, version identifiers | Delivery index, version chain, handoff status | Designing individual artifacts |
| 数据质量、异常数据、缺失值、重复、口径校验、对账规则 | `$data-quality-validation` | Source/model/API samples, quality rules, expected thresholds | Quality rules, validation result, remediation plan | Visual component styling |
| 权限矩阵、角色权限、数据权限、字段权限、操作权限 | `$permission-matrix-validation` | Role/user matrix, data scope, API/page actions | Permission matrix, cases, gaps | General SSO login flow only |
| 报表设计系统、组件规范、模板治理、样式一致性 | `$report-design-system-governance` | Existing templates/components, target brand/system | Design tokens, component/template governance, usage rules | Single page business analysis |
| 上线后监控、反馈闭环、运行问题、指标使用效果、持续优化 | `$production-observability-feedback` | Release/runtime evidence, monitoring/user feedback | Observability plan, feedback log, optimization backlog | Pre-release prototype only |

## Stage Handoff Requirements

Every stage output must include:

- `Artifact readability`: confirm the artifact is human-first and AI-extractable, or state why separate human/machine outputs were created.
- `Stage`: workflow name.
- `Artifact version/source`: file paths, source URLs, commit, or user-provided document names when known.
- `Delivery version chain`: upstream/downstream version mapping when the artifact participates in an iteration or release.
- `Code file ledger`: for source-code changes, list changed code files, sidecar ledger paths, pre-change read/create status, appended version, changed ranges/stable anchors, affected contracts, and verification.
- `Entry consistency`: `pass`, `partial`, `blocked`, or `not needed`, with unresolved `ENTRY-*` IDs when applicable.
- `Design reasonableness`: `pass`, `partial`, `blocked`, or `not needed`, with unresolved `DESIGN-*` IDs when applicable.
- `Production closed loop`: `ready`, `partial`, `blocked`, or `not needed`, with missing production controls or open retest items when applicable.
- `Environment profile`: `test`, `production`, `not needed`, or `blocked`, plus the config file loaded (`.env.test` or `.env.production`) when runtime behavior is in scope.
- `Report data-visualization frontend`: `ready`, `partial`, `blocked`, or `not needed`, with missing purpose/hierarchy/chart-choice/metric-format/filter/interaction/state/provider/performance/theme/runtime-QA decisions when report frontend visualization is in scope.
- `Report integration testing`: `ready`, `partial`, `blocked`, or `not needed`, with missing metric口径/golden-data/reconciliation/API/frontend/filter/permission/cache/export/performance/UAT/smoke/monitoring/rollback/regression/retest decisions when report integration or production acceptance is in scope.
- `Performance/resilience`: `ready`, `partial`, `blocked`, or `not needed`, with missing concurrency/cache/pool/timeout/observability decisions when applicable.
- `Report data-service backend`: `ready`, `partial`, `blocked`, or `not needed`, with missing metadata/query-chain/permission/guardrail/export/audit/freshness/governance decisions when report backend APIs are in scope.
- `SQL query optimization`: `ready`, `partial`, `blocked`, or `not needed`, with missing projection/predicate/join/pagination/plan-evidence decisions when database-backed APIs are in scope.
- `Data modeling`: `ready`, `partial`, `blocked`, or `not needed`, with missing business question/process/grain/layer/metric-additivity/history/quality/lineage decisions when OLAP/reporting models are in scope.
- `Readiness`: one of `ready`, `partial`, or `blocked`.
- `Assumptions`: accepted temporary assumptions with affected artifacts.
- `Blockers`: missing item, impact, owner/source needed, and next question.
- `Next stage`: intended consuming workflow and what it can use directly.
- `Out of scope`: work intentionally deferred.

## Readiness Values

Use these values consistently:

- `ready`: The next stage can proceed without inventing core business, data, auth, environment, or testing behavior.
- `partial`: The next stage can proceed with explicit assumptions or limited scope; unresolved items are non-blocking for the stated target.
- `blocked`: The next stage cannot produce a reliable result until listed blockers are resolved.
- `not run`: Runtime validation was applicable but could not be executed. Use only in testing/verification sections, not as an artifact readiness value.

Do not mark an artifact `ready` when a P0 metric, API, data source, permission rule, SSO contract, or runtime URL required by the next stage is unknown.

Do not mark an artifact `ready` when filter linkage evidence skipped the data-completeness-first gate. For any affecting primary/global filter, option data, fact/business rows or provider responses, required fields, default/non-default states, and resolver/API branches must be checked before filter binding is accepted.

Do not mark an artifact `ready` when snapshot/latest-period API groups lack an explicit snapshot role and data-version contract, when data-version/business/permission scope is not enforced through backend params, source predicates, precompute lookup keys, snapshot reuse rules, or cache keys, or when a metrics/trend/ranking/table/drilldown/export endpoint depends on an undocumented snapshot/dashboard endpoint response, frontend call order, controller memory, or app-memory payload.

Do not mark an artifact `ready` when a source/table/upstream/fixture replacement silently changes existing API response fields or behavior, or when new response fields are not additive, named by convention, source-traced, permission-aware, and contract-validated.

Do not mark an artifact `ready` when Redis/cache is required or named for production-bound data services but role, key template, TTL/invalidation, permission-safety dimensions, miss/stampede behavior, fallback, pool/timeouts, and observability are missing.

Do not mark an API inventory or API document `ready` for backend implementation when production-bound endpoints lack a backend reuse pattern, common request/response model family, service-layer mapping, or an explicit reason for custom controller/query/DTO shapes.

Do not mark an artifact `ready` when an unresolved `P0` or `P1` `ENTRY-*` conflict affects the next stage's scope, source authority, metric口径, API contract, permission/auth behavior, environment, or runtime data path.

Do not mark an artifact `ready` when an unresolved `P0` `DESIGN-*` finding exists, or when an unresolved `P1` `DESIGN-*` finding would affect user-visible behavior, data correctness, API/model feasibility, permissions, layout comprehension, or testability in the next stage.

Do not mark a production-bound artifact `ready` when required source authority, runtime URL/health, auth/permission, deployment/config, observability, performance/resilience/capacity, testing evidence, or blocker/major/high defect retest closure is missing.

Do not mark implementation, repair, or runnable prototype handoff `ready` when any changed scoped code file lacks a sidecar code ledger, pre-change read evidence, or a post-change version entry with changed code ranges, modified content, affected contracts, and verification/blocker.

## Cross-Stage Artifact Contract

### Report Design To Technical Solution

Required handoff bundle when a prototype feeds technical solution:

- Prototype theme, user scenario, report type, and core business questions.
- Component binding matrix: component ID, business question, data source, row grain, required fields, controls, filters, `controlSemantics`, `componentSchemaImpact`, navigation metric lineage, interactions, and empty state.
- Mock/data-source contract: dataset IDs, field names, sample rows, formulas, units, enums, and derived values.
- Control/filter contract: perspective switches, global filters, local filters, drilldown params, filter IDs, defaults, option source, field/query mapping, global SQL/source execution stage, component-internal local filter scope, affected components, permission behavior, schema impact, navigation indicator lineage, and bounded-local exception if any.
- Interaction contract: event names, payload fields, target drawer/modal/route/export/action, stale-selection behavior.
- Visual/layout constraints that affect data shape or export behavior.
- Assumptions and gaps that affect model/API design.

### Technical Solution To Backend Development

Required handoff bundle:

- `API清单` with API ID, page/module, method/path candidate, purpose, trigger, request params, response model, auth, priority, and status.
- Backend-friendly API design evidence: reuse pattern, common request model, response envelope/model family, service-layer mapping, and custom-shape reason when applicable.
- `数据模型文件` with source/logical/response models, fields, formulas, joins, ownership, freshness, permission and quality rules.
- Source replacement/API response compatibility plan when source changes are possible: unchanged response fields, old/new source-field mapping, additive fields, naming convention, transformation/default/null rules, version/deprecation decisions, and contract validation scope.
- OLAP modeling evidence when reporting/BI/dashboard metrics are in scope: business question matrix, subject areas, business processes, model layer/type, one-grain-per-model decision, conformed dimensions, metric additivity, time口径, summary/wide-table decisions, history/SCD, many-to-many, deduplication, late-arriving/backfill, and lineage.
- `待补充数据模型清单` with `GAP-*` IDs, impact, owner questions, assumptions, and blocked/partial status.
- Parameter-driven data-version and snapshot reuse contract when snapshot/latest-period semantics exist: snapshot role, `snapshotDate`, `latestPeriod`, `loadBatch`, `dataVersion`, report/source version, exposing endpoint or metadata source, consuming/reusing endpoints, backend query params, permission/data-scope params, source predicate/precompute/snapshot lookup mapping, cache-key dimensions, invalidation trigger, and proof that any cross-endpoint reuse is declared rather than hidden runtime payload or application-memory snapshot.
- Filter/sort/page execution evidence: API rows and models must state whether global filters, sorting, pagination, ranking, grouping, aggregation, Top/Bottom, and counts run in SQL/source/provider/repository/precompute/cache, and must not rely on page/API-level full-materialize-then-filter behavior. Component-internal filters must be separately scoped to already fetched component data.
- Performance/resilience plan: expected volume/latency, concurrency model, cache/precompute strategy, Redis role/key/TTL/invalidation/fallback decisions when used, connection/resource pools, async/offline job strategy for long-running work, timeout/retry/circuit-breaker behavior, rate/concurrency limits, health/readiness, observability, and unresolved risks.
- Report data-service backend plan when report/BI/dashboard APIs are in scope: report type, metadata/query-chain ownership, parameter guardrails, permission/tenant/field/export behavior, component-ready response rule, pagination/count/export strategy, cache key safety, freshness/quality metadata, audit/monitoring, version/publish/rollback, and unresolved governance gaps.
- Backend reuse plan when report/BI/dashboard APIs are in scope: metadata/filter/query/dashboard/export/action/status API families, shared request models, shared response envelopes, reusable service layers, and one-off endpoint exceptions.
- SQL writing plan for database-backed APIs: required columns, sargable predicates, join keys/cardinality, aggregation-before-join needs, dedup/order necessity, pagination/keyset strategy, dynamic optional-filter strategy, and plan-evidence or slow-query gap IDs.
- Consistency result: every API maps to a response model, and every response field maps to a source/formula/enum/gap.
- Production architecture readiness when intended for real delivery: runtime topology, frontend/backend/data boundaries, source authority, environment/auth/security assumptions, observability/performance/deployment concerns, testing handoff, and open blockers.

### Backend Development To Frontend Development

Required handoff bundle:

- `API文档` with base URL, auth headers, endpoint details, request/response examples, errors, empty/no-permission behavior, pagination/sorting/filter rules, filter/sort/page execution stage, default/max page size, and pending items.
- API response compatibility evidence for any source/table/upstream/fixture replacement: preserved existing fields, additive/new fields, naming compliance, transformation/default/null mapping, and breaking/versioning notes.
- Snapshot/latest-period endpoint docs when applicable: snapshot role, shared data-version fields, defaulting rules, source of truth, request/defaulted/injected params, source predicate/precompute/snapshot lookup mapping, cache-key dimensions, invalidation, and endpoint dependency/reuse rules.
- Runtime backend URL when implementation exists.
- Environment profile contract: `.env.test` and `.env.production` presence, backend/API base paths, source mode, auth/SSO endpoint, CORS allowlist, health/readiness path, and blockers for missing or sensitive values.
- Auth/SSO contract: header names, token rules, 401/token-invalid response, 403 response, public allowlist.
- Backend health/smoke evidence, source-mode proof, environment/config notes, version/API-doc alignment, and deployment/rollback notes when implementation exists.
- Observability and performance/resilience constraints: log/error identifiers, timeout/export limits, expected volume/concurrency, Redis/cache strategy, database/upstream/cache connection-pool behavior, `ApiError`/timeout/exception release/close guarantee, pagination/aggregation constraints, max page size, total-count strategy, source-side/provider-side execution proof, component-local filter boundary, full-materialize-then-filter absence for global scope, async/offline job contract for long-running work, timeout/retry/fallback behavior, rate/concurrency limits, and known capacity risks.
- Report data-service backend constraints when applicable: metadata/report version behavior, dimension/metric/filter/sort whitelists, backend-injected tenant/data permission predicates, parameter guardrails, component-ready result metadata, freshness/quality fields, cache key permission safety, async export lifecycle, query/export/download/config audit, and slow-report governance signals.
- SQL writing constraints for database-backed endpoints: selected columns, direct/type-consistent predicates, avoided functions/casts/arithmetic on filter/join fields, complete join keys, one-to-many handling, `EXISTS`/`NOT EXISTS` use when applicable, `UNION ALL` vs `UNION`, stable/keyset pagination, `WHERE` before `HAVING`, and `EXPLAIN` or slow-query evidence for risky P0 queries.
- Resilience controls when implementation exists: bounded concurrency/thread/worker model, async queue/worker/retry/dead-letter behavior for long-running work, upstream timeout/retry/circuit-breaker/fallback behavior, rate/concurrency limits, pool saturation handling, `ApiError` repeated-failure pool non-exhaustion evidence such as for `STARROCKS_POOL_MAX=5`, cache stampede protection, health/readiness checks, and observability metrics.
- Known partial/blocked endpoints and accepted assumptions.
- Sample responses for frontend adapter validation, plus SQLite fixture/source-mode notes when backend simulation data is used.

### Frontend Development To Testing Integration

Required handoff bundle:

- `前端功能说明` with pages/modules, provider mapping, filters, interactions, states, permissions, exports, verification evidence, and known limitations.
- Report data-visualization frontend evidence: page type, user purpose, first-screen answer, component/chart choice, metric formatting/口径/freshness, control semantics, filter/linkage/drill-through behavior, non-default perspective behavior, cross-perspective consistency, fixed-height navigation/card height budget and DOM overflow evidence, component-ready provider mapping, state coverage, frontend performance controls, theme/accessibility, and known visualization limitations.
- Frontend URL when runnable.
- Backend/API base URL used by the frontend.
- Environment/auth/proxy/deployment notes, including which profile loaded `.env.test` or `.env.production`, whether frontend and backend point to the same intended environment, and any retained mock/demo mode per profile.
- Headless browser screenshot evidence, deterministic baseline diff artifacts / `VDIFF-*` findings, and multimodal `VIS-*` visual findings from runtime QA when visual behavior was verified.
- Known gaps, retained offline/demo sources, and not-yet-verified behaviors.

### Testing Integration To Repair Workflows

Required feedback bundle for every defect:

- Defect ID, severity, likely owner workflow: report design, technical solution, backend, frontend, SSO/security, data, environment, or unclear.
- Expected result, actual result, evidence, reproduction steps, and affected artifact/API/page/component.
- Report integration testing context when applicable: metric口径, golden/baseline dataset, source/model/API/frontend/export reconciliation evidence, account/role/tenant, active perspective, active filters, cache hit/miss status, data freshness time, query/task/export ID, and likely chain layer.
- Screenshot path, baseline/current/diff path when available, deterministic `VDIFF-*` finding, and multimodal `VIS-*` finding when the defect is visual/layout related.
- Retest criteria and required input to unblock.
- Status: `open`, `fixed`, `retest`, `closed`, `blocked`, or `accepted`.
- Retest evidence and environment profile/config file/version for every closed blocker/major/high defect.

### Production Closed-Loop Handoff

Required when the delivery target is real production use, release acceptance, or a production-like pilot:

- Technical architecture: confirmed runtime boundaries, source authority, security/auth assumptions, deployment/config approach, observability, performance/resilience/capacity risks, and testing strategy.
- Data service/backend: API doc version, runtime backend URL or deployment target, health/readiness evidence, authoritative source mode, auth/permission behavior, config/env handling, error/log behavior, performance/resilience/export limits, and rollback notes.
- Report data-service backend: report metadata/query-chain evidence, safe code-to-source query generation, permission/tenant/cache safety, parameter limits, component-ready response/freshness/quality evidence, async export lifecycle, audit/monitoring evidence, and slow-report governance plan when report APIs are in scope.
- Frontend integration: frontend URL/build, backend base URL, environment profile loaded from `.env.test` or `.env.production`, provider mode, SSO/auth behavior, report data-visualization frontend evidence, retained mock/demo sources if any, browser/runtime QA evidence, and known gaps.
- Testing integration: environment profile/config file/version/account/data used, golden/baseline dataset, metric/model/API/frontend/export reconciliation evidence, permission/cache/export/performance/exception/UAT/smoke/regression coverage, executed case counts, evidence paths, defect statuses, retest closure matrix, remaining risks, and final readiness.

If any required production handoff item is unknown, mark production closed loop `partial` or `blocked` and name the owner/source needed.

## Missing Input Handling

When information is missing:

1. Classify severity: `Blocker`, `High`, `Medium`, or `Low`.
2. Decide artifact readiness: `ready`, `partial`, or `blocked`.
3. Record the exact assumption only when safe.
4. Ask one owner/source question for each blocker.
5. Keep the same gap ID and wording across all affected artifacts.

When information is contradictory rather than merely missing, use `$quality-gate-validation` `references/entry-input-consistency-gate.md` and `ENTRY-*` IDs. Do not downgrade a real contradiction into a silent assumption.

When the information is available but the proposed structure is unreasonable, use `$quality-gate-validation` `references/design-reasonableness-gate.md` and `DESIGN-*` IDs. Do not downgrade a design flaw into a vague missing-input item.

## Child Skill Call Checklist

Top-level workflows must call child skills when their trigger conditions are met, and must state why a relevant child skill was skipped when skipping creates risk.

Use this pattern:

```text
Child skill:
Trigger:
Used / skipped:
Reason:
Output or evidence:
```
