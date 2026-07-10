---
name: backend-development-workflow
description: "[后端阶段] 独立承担真实后端/数据服务项目的新建、设计、API文档、接口实现、运行验证和交付，不要求必须先有 prototype。支持 standalone-new-project、existing-project、prototype-derived 三种入口；有 prototype 时消费其 PRD/数据契约，无 prototype 时直接从用户需求、API预期、数据源、权限和环境约束初始化并实现服务。用户提到新建后端项目、后端、服务端、数据服务、接口实现/开发、API文档、Python/Flask、Java/Spring Boot、数据库/上游API、连接池/Redis、鉴权、Haier IAMA、启动后端、本地URL或mock转真实接口时触发。"
---

# Backend Development Workflow

## Stage Scope

Classification: 后端阶段.

Use this copy only inside the backend/data-service skill bundle. Treat frontend, prototype, and testing work as contracts, evidence, handoff notes, or blockers; do not edit those stages from this skill.

## Positioning

Use this workflow as the independent entry point for real backend/data-service development. It can initialize a new runnable service from user requirements and source/API evidence, continue an existing backend, or consume a completed prototype handoff. A prototype is one possible input, never a universal prerequisite.

It owns data-service runtime boundaries, route/service/query layering, contracts, transformation adapters, pools/cache/precompute, permissions, logging/observability, environment, deployment, and backend readiness.

For `prototype-derived` work, targeted reading and prototype data summary are first-class inputs. For `standalone-new-project`, source objects, representative content, consumer/API expectations, business rules, permissions, and environment constraints are the authority. In every mode, backend work must not derive production APIs from UI labels alone.

## Reference Files

- `references/00-prototype-downstream-handoff-contract.md` is mandatory for prototype-derived backend work. It defines the fixed PRD/child-backend baseline, prototype version, stable-ID consumption, source-authority rules, mock replacement, configuration trace, minimal-interface boundary, and readiness evidence.
- `references/01-standalone-new-project-contract.md` is mandatory when no prototype or existing backend target exists. It defines greenfield stack/project setup, service/API/source matrices, vertical-slice implementation, tests, runtime, and readiness.
- `references/data-service-design-template.md` for backend/data-service design output.
- `references/api-document-template.md` for API documentation.
- `references/report-data-service-backend-implementation.md` for implementation details.
- `references/minimal-interface-implementation-principles.md` for interface implementation's default simple mode: filters as request params, table-content understanding before work, and query-only retrieval without hidden aggregation or processing.
- `references/missing-info-template.md` for blocked or partial backend handoff.
- `references/backend-development-gates.md` for detailed constraints, required outputs, and readiness blockers.
- Upstream report handoff: `prd/execution/prd-targeted-reading-analysis.md`, `docs/prototype-data-summary.md`, `prd/execution/prd-data-api-contract.md`, `prd/execution/prd-metric-dictionary-and-mounting.md`, `prd/execution/prd-interaction-contract.md`, and `prd/children/prd-child-backend.md` when present.
- `$quality-gate-validation` `references/preflight-understanding-gate.md` before backend design, API docs, implementation, repair, or readiness.

## Child Skills

| Stage | Skill |
| --- | --- |
| Python Flask SSO multi-database architecture | `$python-flask-sso-multidatabase-backend` |
| Java Spring Boot backend architecture | `$java-springboot-backend-development` |
| API documentation | `$api-documentation-design` |
| API contract validation | `$api-contract-validation` |
| Data model/source mapping | `$data-model-source-mapping` |
| Transformation adapters | `$data-transformation-adapter-design` |
| Performance and Redis/cache/pool design | `$performance-optimization` |
| SSO/auth integration | `$haier-sso-integration` |
| Runtime URL smoke test | `$runtime-url-smoke-test` |
| Production observability | `$production-observability-feedback` |
| Code file ledgers | `$code-change-ledger-management` |
| Delivery/version index | `$delivery-version-management` |
| Metric number display | `$metric-number-display-contract` |
| Environment profile contract | `$environment-profile-contract` |
| Quality gates | `$quality-gate-validation` |

## Data-Service Architecture Scope

Decide endpoint families, request context, response envelope, service/query/source-adapter layers, transformation boundaries, data-version/snapshot role, filters/pagination/sorting/export scope, permission injection, pool/cache/precompute strategy, error model, logging, health/status endpoints, deployment, and rollback.

## Workflow

1. Run the Preflight understanding gate before backend design, API docs, implementation, or repair. Name the requested stage, evidence inventory, source/API/model/frontend authority order, affected contracts, owning skills, missing evidence, and start decision.
2. Classify `backendEntryMode` as `standalone-new-project`, `existing-project`, or `prototype-derived`. Prototype absence must select the standalone path when the requested deliverable is backend development; it must not redirect the task to prototype generation.
3P. For `prototype-derived`, load `references/00-prototype-downstream-handoff-contract.md`, create the prototype baseline and stable-ID consumption/trace/replacement matrices, and preserve handoff ownership.
3S. For `standalone-new-project`, resolve the writable root, load `references/01-standalone-new-project-contract.md`, create `standaloneBackendBaseline`, `serviceBoundaryMatrix`, `apiContractMatrix`, `sourceObjectUnderstandingMatrix`, `requestParamPredicateMatrix`, and `implementationVerificationMatrix`, then initialize the real service.
3E. For `existing-project`, inspect and preserve the authoritative stack, modules, response/error contracts, auth, persistence, migrations, tests, configuration, and runtime conventions; create only missing bounded planning rows.
4. Run quality gates when targeted reading, source/API/model/frontend expectations conflict.
5. Run the anti-laziness execution gate from `$quality-gate-validation` for implementation, repair, documentation, or acceptance steps. Keep `LAZY-*` findings visible until evidence closes them.
6. Apply the minimal interface implementation principles before endpoint design or code edits. For every involved table/view/fixture/upstream object, create `tableContentUnderstandingMatrix` from representative content, row grain, keys, filter fields, permission fields, result bounds, nulls, and gaps; create `requestParamPredicateMatrix`; default repository access to projection + predicates + stable order + bounded pagination. Do not add hidden joins, aggregation, formulas, totals, rankings, exact counts, broad in-memory filtering, or response reshaping for simple table retrieval.
7. Define data-service design: boundaries, layers, request context, response model, numeric metadata contract, data-version contract, permission scope, SSO/auth flow, database ownership, cache/precompute, and observability. Use mock-to-real mapping only for prototype/mock-derived scope; use `apiContractMatrix` and source matrices for standalone scope. Load the Python/Flask or Java/Spring Boot child skill according to stack selection.
8. Produce or update API documentation through `$api-documentation-design`.
9. Validate contracts against the active entry mode's authority: prototype rows for `prototype-derived`, `apiContractMatrix` plus source evidence for `standalone-new-project`, or existing docs/code/runtime behavior for `existing-project`.
10. Design transformation adapters for source-to-response and response-to-view-model compatibility only after proving the simple query boundary is insufficient or the mapping is only field-alias/serializer compatibility. Do not use adapters to hide business aggregation or missing filter params.
11. If implementation is requested, edit backend code with `$code-change-ledger-management` discipline and preserve existing project patterns.
12. Configure pools, Redis/cache, timeouts, errors, logging, health checks, and env profiles. Use `$redis-cache-design-patterns` when Redis is named and `$environment-profile-contract` when handoff profiles matter.
13. Run available tests/build/startup and `$runtime-url-smoke-test` when a URL is produced.
14. Produce backend handoff notes, gaps, readiness, and version links.

## Required Output

- Preflight understanding matrix and backend/data-service design or implemented service summary.
- `backendEntryMode` and its governing contract.
- For `standalone-new-project`: `standaloneBackendBaseline`, `serviceBoundaryMatrix`, `apiContractMatrix`, `sourceObjectUnderstandingMatrix`, `requestParamPredicateMatrix`, and `implementationVerificationMatrix`.
- For `prototype-derived` only: targeted reading, prototype handoff/data-summary evidence, prototype baseline, `prototypeContractConsumptionMatrix`, `prototypeConfigurationTraceMatrix`, and `mockToRealBackendMatrix`.
- API documentation/contract status.
- Python/Flask SSO and multi-database architecture when applicable: app factory, route/service/repository/db layers, token validation, 401/403, database role map, env vars, and pool ownership.
- Java/Spring Boot architecture when applicable: controller/service/mapper-or-repository layering, `ApiResponse<T>`, global exception handling, Spring Security/JWT/SSO, IAM/IAMA or local JWT bridge, Profile YAML, Maven/Gradle, Docker, and startup commands.
- Source/model/adapter mapping and response compatibility notes.
- Minimal interface proof: table-content understanding matrix for every involved source object, request-param-to-source-field mapping, query-only proof, absence of hidden aggregation/processing, and open `GAP-*` rows.
- Mock-to-real backend mapping: mock endpoint/data source/component data key, target real API, request DTO, response DTO, source/model dependency, service method, frontend consumer, filter/interaction/conclusion-rule impact, permission/cache/error behavior, and verification.
- Numeric precision/display contract: value type, raw/display unit, scale, precision, tooltip/export precision, rounding, null/zero/denominator-zero, and data-vs-presentation ownership.
- Runtime model: pools, Redis/cache/precompute, timeout/fallback, export/async behavior, env/auth, health, logging, observability.
- Code-ledger proof when backend source changed.
- Anti-laziness execution result: local evidence inspected, `LAZY-*` findings or explicit no-finding result, before/after proof for repairs, regression probe, and readiness impact.
- Verification commands, URL/smoke result, blockers, and readiness.

## Quality Gate

- Do not implement routes from UI fields alone; trace endpoints to source/model/metric/permission contracts.
- Do not require a prototype, prototype PRD, configured prototype project, or prototype data summary for `standalone-new-project` or ordinary `existing-project` backend development.
- Do not implement or document table-backed interfaces before understanding every involved table's content, grain, keys, filter fields, samples, result bounds, and permission fields.
- Do not mark interface implementation ready when client-visible filters are hidden in controller/service code instead of being request params mapped to source predicates.
- Do not add aggregation, totals, rankings, formula calculation, broad in-memory processing, or unproven multi-table joins to a simple table retrieval endpoint. Query source-aligned rows first; route aggregate needs to explicit model/precompute/design work.
- Do not implement or document prototype-derived backend behavior when `prd/execution/prd-targeted-reading-analysis.md` is missing, generic, lacks source-material/evidence-to-decision trace, or is not consumed by API/model/runtime choices.
- Do not implement or document prototype-derived report APIs without consuming `docs/prototype-data-summary.md` and the PRD data/API execution files when they exist.
- Do not start prototype-derived endpoint design when the fixed PRD core or `prd/children/prd-child-backend.md` is missing/stale, strict PRD validation is unrecorded, prototype version/source authority is unknown, or affected replacement rows lack bounded backend ownership.
- Do not mark mock-to-real replacement ready when affected mock endpoints, component data keys, filters, interactions, exports, drilldowns, or conclusion-rule inputs lack replacement-matrix rows or explicit `GAP-*` blockers.
- Do not mark backend work ready when any accepted prototype `API-*`, `OBJ-*`, `MET-*`, `FILTER-*`, `INT-*`, or `RULE-*` row lacks API/source/code/test trace, or when page/block/slot layout semantics have leaked into endpoint design.
- Do not implement or document backend behavior before a Preflight understanding decision identifies source authority, API/model/frontend contracts, runtime target, and blockers.
- Existing API response fields are stable across source/table/upstream replacement unless a versioned breaking change is documented.
- Existing numeric response semantics are stable across source/table/upstream replacement: type, raw unit, display unit, scale, precision, formula, nullability, denominator-zero behavior, and export precision cannot drift without a versioned change.
- Python/Flask SSO + multi-database backends must separate API, service, repository, db engine/session, middleware, schema, and SQL-file responsibilities; do not place complex SQL, token validation, permission checks, and response formatting all inside route handlers.
- Java/Spring Boot backends must keep controllers thin, place transactions in service implementations, separate DTO/Entity/VO, define global exception handling, and keep JWT/SSO/Security behavior out of business controllers.
- SSO readiness requires backend token validation, clear `Access-Token`/optional `Application-Key` header contract, distinct 401 and 403 behavior, local user/role/permission mapping, and token/log redaction.
- Data-bearing endpoints must use request/defaulted version params, backend-injected permission/data scope, source predicates or cache/precompute keys; echoing metadata is not enough.
- Backend/data-service readiness needs diagnosable structured logs, connection release on errors/timeouts, env separation, and runtime verification.
- Do not mark backend work ready when the anti-laziness gate is missing, `LAZY-*` findings remain open, or the conclusion uses generic "checked/done/optimized" wording without concrete evidence.
- Load `backend-development-gates.md` before implementing, documenting, or accepting backend/data-service work.
