---
name: backend-development-workflow
description: "[后端阶段] 本阶段版本仅服务后端/数据服务设计、API文档/契约、接口实现、运行验证和后端交付；不承接原型设计、前端代码或测试执行。运行数据服务/后端阶段，把技术方案、API清单、数据模型、prototype 输出的 prd/execution/prd-targeted-reading-analysis.md、docs/prototype-data-summary.md、Mock API To HTTP API Replacement Matrix 和 Metric To Interface And Source Mapping 转成数据服务设计、API文档，或在用户明确要求时实现后端接口和本地服务。用户提到后端、服务端、数据服务、接口实现/接口开发、API文档、默认后端技术栈、Python/Flask、Java/Spring Boot、连接池/Redis、快照接口、snapshotDate/dataVersion/loadBatch、筛选前数据完整性、数据库/上游API接入、响应字段兼容、新增字段命名、鉴权中间件、Haier IAMA、启动后端、本地后端URL、mock转真实接口时触发。"
---

# Backend Development Workflow

## Stage Scope

Classification: 后端阶段.

Use this copy only inside the backend/data-service skill bundle. Treat frontend, prototype, and testing work as contracts, evidence, handoff notes, or blockers; do not edit those stages from this skill.

## Positioning

Use this workflow for the backend/data-service stage: convert a technical solution, API inventory, data model, source mapping, executable PRD data/API contract, or prototype-data-summary handoff into a backend design, API documentation, implementation plan, or runnable backend service when explicitly requested.

It owns data-service runtime boundaries, route/service/query layering, contracts, transformation adapters, pools/cache/precompute, permissions, logging/observability, environment, deployment, and backend readiness.

For report/dashboard/cockpit/detail/analysis/self-service work, `prd/execution/prd-targeted-reading-analysis.md` and `docs/prototype-data-summary.md` are first-class backend inputs. Targeted reading rows must decide which source materials are authoritative, what not to infer, and which `ENTRY-*` / `GAP-*` rows affect API/model choices. The data summary must drive mock-to-real endpoint replacement, component-ready response shape, filter params, interaction payloads, conclusion-rule inputs, backend method candidates, and gaps. Backend work must not derive production APIs from UI fields alone.

## Reference Files

- `references/data-service-design-template.md` for backend/data-service design output.
- `references/api-document-template.md` for API documentation.
- `references/report-data-service-backend-implementation.md` for implementation details.
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
2. Inventory technical solution, API inventory, model/source mapping, `prd/execution/prd-targeted-reading-analysis.md`, upstream PRD data/API files, `docs/prototype-data-summary.md`, Mock API To HTTP API Replacement Matrix, Metric To Interface And Source Mapping, component data keys, filters, interactions, conclusion inputs, metric口径, numeric display/precision contracts, permissions, SSO/token header contract, database role map, env/auth, and existing code. Use `$metric-number-display-contract` for numeric semantics and `$environment-profile-contract` for test/production runtime profiles when in scope.
3. For PRD/prototype-derived backend work, consume targeted reading rows before endpoint/model design: cite relevant `SRC-*`, `READ-*`, `ENTRY-*`, and `GAP-*` rows, decide source authority, note non-authority materials, and connect each backend decision to a row or blocker.
4. Run quality gates when targeted reading, source/API/model/frontend expectations conflict.
5. Run the anti-laziness execution gate from `$quality-gate-validation` for implementation, repair, documentation, or acceptance steps. Keep `LAZY-*` findings visible until evidence closes them.
6. Define data-service design: boundaries, layers, request context, response model, numeric metadata contract, data-version contract, permission scope, SSO/auth flow, database ownership, cache/precompute, and observability. For prototype-derived work, create a mock-to-real mapping for every affected mock endpoint/data source/component data key before endpoint design. Load `$python-flask-sso-multidatabase-backend` when Python/Flask SSO or multi-database structure is in scope; load `$java-springboot-backend-development` when Java/Spring Boot structure, Spring Security/JWT/SSO, Maven/Docker, or Profile conventions are in scope.
7. Produce or update API documentation through `$api-documentation-design`.
8. Validate contracts against frontend expectations, targeted reading rows, source samples, OpenAPI, mocks, prototype-data-summary rows, PRD data/API rows, routes, and runtime responses.
9. Design transformation adapters for source-to-response and response-to-view-model compatibility.
10. If implementation is requested, edit backend code with `$code-change-ledger-management` discipline and preserve existing project patterns.
11. Configure pools, Redis/cache, timeouts, errors, logging, health checks, and env profiles. Use `$redis-cache-design-patterns` when Redis is named and `$environment-profile-contract` when handoff profiles matter.
12. Run available tests/build/startup and `$runtime-url-smoke-test` when a URL is produced.
13. Produce backend handoff notes, gaps, readiness, and version links.

## Required Output

- Preflight understanding matrix and backend/data-service design or implemented service summary.
- Targeted reading consumption: `prd/execution/prd-targeted-reading-analysis.md` status, consumed `SRC-*` / `READ-*` rows, backend-relevant evidence-to-decision trace, non-authority notes, and open `ENTRY-*` / `GAP-*`.
- Upstream prototype handoff consumption: targeted reading rows, `docs/prototype-data-summary.md` status, Metric To Interface And Source Mapping coverage, Mock API To HTTP API Replacement Matrix coverage, component data key coverage, `prd-data-api-contract` coverage, and unresolved `GAP-*` rows.
- API documentation/contract status.
- Python/Flask SSO and multi-database architecture when applicable: app factory, route/service/repository/db layers, token validation, 401/403, database role map, env vars, and pool ownership.
- Java/Spring Boot architecture when applicable: controller/service/mapper-or-repository layering, `ApiResponse<T>`, global exception handling, Spring Security/JWT/SSO, IAM/IAMA or local JWT bridge, Profile YAML, Maven/Gradle, Docker, and startup commands.
- Source/model/adapter mapping and response compatibility notes.
- Mock-to-real backend mapping: mock endpoint/data source/component data key, target real API, request DTO, response DTO, source/model dependency, service method, frontend consumer, filter/interaction/conclusion-rule impact, permission/cache/error behavior, and verification.
- Numeric precision/display contract: value type, raw/display unit, scale, precision, tooltip/export precision, rounding, null/zero/denominator-zero, and data-vs-presentation ownership.
- Runtime model: pools, Redis/cache/precompute, timeout/fallback, export/async behavior, env/auth, health, logging, observability.
- Code-ledger proof when backend source changed.
- Anti-laziness execution result: local evidence inspected, `LAZY-*` findings or explicit no-finding result, before/after proof for repairs, regression probe, and readiness impact.
- Verification commands, URL/smoke result, blockers, and readiness.

## Quality Gate

- Do not implement routes from UI fields alone; trace endpoints to source/model/metric/permission contracts.
- Do not implement or document prototype-derived backend behavior when `prd/execution/prd-targeted-reading-analysis.md` is missing, generic, lacks source-material/evidence-to-decision trace, or is not consumed by API/model/runtime choices.
- Do not implement or document prototype-derived report APIs without consuming `docs/prototype-data-summary.md` and the PRD data/API execution files when they exist.
- Do not mark mock-to-real replacement ready when affected mock endpoints, component data keys, filters, interactions, exports, drilldowns, or conclusion-rule inputs lack replacement-matrix rows or explicit `GAP-*` blockers.
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
