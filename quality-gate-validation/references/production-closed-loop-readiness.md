# Production Closed Loop Readiness

Use this reference for technical architecture, data-service/backend, frontend integration, and testing-integration workflows when artifacts are expected to support real production delivery rather than only a prototype, demo, or one-off document.

The goal is to make the architecture/technology decision/implementation roadmap -> data service -> frontend integration -> testing -> defect repair -> retest loop explicit and usable in production.

## Closed Loop Model

Production delivery is closed only when these links are traceable:

1. Requirement/prototype contract -> technical architecture.
2. Technical architecture -> technology selection/ADR, implementation roadmap, API inventory, data model, source strategy, runtime/security decisions, and risk/gap ledger.
3. API inventory + data model -> data-service design, API documentation, and backend implementation.
4. Backend implementation -> contract validation, runtime URL, health/smoke evidence, and consumer examples.
5. Frontend integration -> function description, runtime URL, API base, environment profile, auth/env notes, and visual/runtime QA evidence.
6. Testing integration -> executable cases, evidence-backed results, defects routed to owner workflows.
7. Repair workflow -> retest evidence, status update, and closure criteria.

For any stage that creates or changes frontend, backend, or runnable prototype source code, file-level code change ledgers are part of the closed loop. Each changed scoped code file must have a sidecar ledger that was read before editing and appended after editing with version, feature list, changed code ranges, affected contracts, verification, and rollback notes.

If any link is missing, the stage may still be `partial`, but it is not production-closed.

## Production Readiness Dimensions

Check these dimensions before marking a technical solution, data service, or testing package `ready` for production:

- Architecture decision: selected runtime topology, service boundary, data flow, dependency ownership, and why alternatives were rejected when relevant.
- Authoritative data source: source system/table/API/file owner, access method, refresh cadence, quality rule, fallback behavior, and sample evidence.
- API/model contract: endpoint boundary, request params, response model, transformations, error envelope, pagination/sorting/export, default/max page size, stable ordering, global SQL/source-side/provider-side filter execution, component-internal local filter scope, parameter-driven data-version/scope filtering, versioning, and backward compatibility.
- Report data-service backend readiness: apply `$backend-development-workflow` for report/BI/dashboard APIs; report metadata, backend reuse pattern/API family, common request/response model family, parameter-driven query context, query-service chain, dimension/metric/filter/sort whitelists, backend-owned source/SQL expression mapping, parameter guardrails, backend-injected tenant/data/field/export permissions, component-ready result metadata, data-vs-presentation boundary, data freshness/quality status, async export lifecycle, Redis/cache role and permission safety when used, audit, version/publish/rollback, and slow-report governance are documented or implemented.
- OLAP data model readiness: apply `$performance-optimization` for reporting/BI/dashboard models; business questions, subject areas, business processes, grains, fact/dimension/summary/application model types, metric additivity, time口径, conformed dimensions, SCD/history, many-to-many handling, update/backfill mode, quality rules, and lineage are documented.
- Security and permissions: SSO/auth, token/header rules, row/field/operation permission, masking, audit log, no-permission behavior, secret/config handling.
- Environment and deployment: `.env.test` and `.env.production` profiles, dev/test/prod base URLs, config variables, proxy/CORS, route/base path, deployment target, startup command, health endpoint, rollback or restore path. Apply `$environment-profile-contract`; a single shared `.env` keeps production readiness `partial` or `blocked` unless the target is explicitly non-production.
- Report data-visualization frontend readiness: apply `$frontend-development-workflow` for report/BI/dashboard frontends; user purpose, first-screen conclusion, chart/table choice, metric formatting/口径, filters/linkage/drill-through, provider mapping, state coverage, freshness/quality display, frontend performance controls, theme/accessibility, and runtime QA evidence are documented or implemented.
- Report integration testing readiness: apply `$testing-integration-workflow` for report/BI/dashboard integration, UAT, release acceptance, or retest closure; metric口径, golden/baseline data, model reconciliation, API/backend behavior, frontend binding, filters, permissions, cache isolation, export parity, performance/stability, exception states, UAT/smoke, monitoring, rollback, regression, automation scope, and defect retest evidence are documented or executed for the stated scope.
- Reliability and observability: logging, request IDs, metrics, traces, health checks, timeout/retry, upstream failure handling, alert owner, and SLA/SLO where needed.
- Code change traceability: every changed frontend/backend/prototype source file has a sidecar `__change_logs__/<file>.changes.md` ledger, pre-change read evidence, post-change version entry, changed code ranges/stable anchors, affected API/props/events/env/data/filter/logging contracts, verification, and rollback notes.
- Backend logging depth: structured backend logs include requestId/traceId, service/env/version, route/method/status/latency, safe user/tenant/role hash where allowed, report/widget/query/dataVersion context when relevant, cache/source/pool/export/job indicators, sanitized error code/summary, redaction rules, slow-query/report thresholds, and log level/config controls.
- Performance and capacity: apply `$performance-optimization`; expected volume, latency target, concurrency/thread/worker model, Redis/cache/precompute rule with key/TTL/invalidation/fallback/observability details when used, pagination/export limits, max page size, total-count strategy, source-side filter/sort/page execution, component-local filter boundary, database/upstream/cache connection-pool behavior including `ApiError`/timeout/exception release/close evidence, full-materialize-then-filter absence for global scope, slow-query risk, async/offline job strategy for long-running work, timeout/retry/circuit-breaker/fallback behavior, rate/concurrency limits, overload handling, and batch/async behavior.
- SQL query readiness: apply `$performance-optimization` for database-backed data-service APIs; projection, sargable predicates, join cardinality, dedup/order necessity, pagination/keyset strategy, aggregation/window placement, dynamic filter generation, and `EXPLAIN` / slow-query evidence are documented for risky P0/high-volume queries.
- Testability: seed data, SQLite fixture database when simulated API data is used, test account/role, executable case matrix, smoke checks, API/display consistency checks, filter/pagination/permission/export cases, and visual regression evidence.
- Defect closure: every blocker/major defect has owner, reproduction, expected/actual, evidence, fix location, retest criteria, and final status.

## Minimal Production Skill Chain

Using fewer skills is acceptable only when the skipped areas are truly out of scope or already proven by evidence. For production-bound delivery, these skill groups form the minimal closed loop:

| Stage | Minimal skill chain | Production risk if skipped |
| --- | --- | --- |
| Requirement and technical architecture | `$report-requirement-structure-extraction`, `$technical-solution-workflow`, `$data-model-source-mapping`, `$api-inventory-design` | API/model artifacts may be traceable on paper but miss business scope, architecture boundaries, technology choices, implementation route, source authority, permissions, runtime/security, or model gaps. |
| Data service and backend | `$backend-development-workflow`, `$api-documentation-design`, `$data-transformation-adapter-design` when mappings/formulas differ, `$api-contract-validation`, `$gap-ledger-management`, SSO skill when auth is in scope | API docs or services may run locally but lack data-service design, authoritative source, query-service chain, auth/config, runtime evidence, or contract proof. |
| Frontend integration handoff | `$api-contract-validation`, `$data-transformation-adapter-design` when provider shape differs, `$frontend-env-deployment-verification`, `$frontend-runtime-qa-validation`, `$frontend-function-description-documentation` | Testing may receive a URL without knowing provider mode, retained mocks, auth/env behavior, visual/runtime evidence, or blockers. |
| Testing and release acceptance | `$integration-test-case-design`, `$runtime-url-smoke-test`, `$sso-auth-flow-test` when auth is in scope, `$frontend-backend-data-consistency-test`, `$filter-linkage-completeness-test`, `$test-evidence-defect-reporting` | Results may become a one-time smoke report instead of report integration acceptance with golden/baseline data, reconciliation, permission/cache/export/performance coverage, evidence, owner routing, and retest closure. |

Do not add child skills mechanically. Add the skill when its trigger condition exists; otherwise record why the area is out of scope, already evidenced, or intentionally deferred.

## Status Rules

- `ready`: all production readiness dimensions needed by the stated scope are confirmed, implemented or documented, and tested enough for the next stage to proceed without inventing behavior.
- `partial`: the stage can proceed for limited scope or non-prod/demo use, with named assumptions, accepted risks, or missing production controls.
- `blocked`: a missing or failed production readiness item prevents reliable downstream use.

Do not mark production readiness `ready` when any of these are unknown for a production-bound scope: authoritative source, P0 metric口径, auth/permission, API version/contract, runtime URL/health, `.env.production` profile/config evidence, report data-visualization frontend evidence when report UI is in scope, report integration testing evidence when report acceptance is in scope, performance/resilience decisions, rollback path, or retest criteria for open blocker/major defects.

Do not mark implementation readiness `ready` when changed frontend/backend/prototype code files lack sidecar code ledgers with pre-change read evidence and post-change version entries. Do not mark backend/data-service production readiness `ready` when request/query/cache/pool/export/error logs cannot be correlated by requestId/traceId or are missing redaction and slow-query/report thresholds.

## Required Production Handoff

For technical architecture / technical solution:

- Architecture overview: business capability, system context, logical architecture, service boundary, runtime topology, data flow, dependencies, environments, operations boundary, and key decisions.
- Technology selection/ADR: selected stacks, default/override reasons, tradeoffs, compatibility/test/release impact, and unresolved decisions.
- Implementation roadmap: phase order, owner actions, dependencies, release gate, rollback, migration/backfill when relevant, and acceptance evidence.
- Environment profile plan: `.env.test` and `.env.production`, frontend/backend pairing, source/auth separation, and blockers.
- API inventory, data model, risk ledger, and gap ledger.
- Data modeling readiness: business analysis matrix, source/logical/response models, layer/type/grain decisions, metric additivity/time口径, summary/wide-table decisions, quality rules, and lineage.
- Nonfunctional requirements: auth, permissions, performance/resilience, observability, deployment, rollback, and testability.
- Report data-service backend plan when report APIs are in scope: metadata/query-chain ownership, backend reuse pattern/API family, common request/response model family, parameter guardrails, permission/tenant/field/export rules, Redis/cache/export/audit/freshness behavior, version/publish/rollback, and slow-report governance.
- Production readiness status and blockers.

For data service / backend:

- Data-service design: service boundary, layered architecture, query-service chain, QueryContext, source-adapter mapping, cache/precompute, async/export, permission/security, observability, deployment/rollback, and handoff readiness.
- API document and implementation status.
- Runtime backend URL or startup blocker.
- Health/smoke evidence, contract validation, source mode, transformation validation, auth behavior, and missing-info document.
- Report data-service backend evidence when applicable: report metadata/version source, query-chain layer mapping, whitelist and parameter validation behavior, permission/tenant/cache safety, component-ready response metadata, freshness/quality fields, export lifecycle, audit logs, and monitoring/slow-report signals.
- Code file ledger proof for changed backend files: ledger path, pre-change read/create status, appended version, route/service/repository/query/logging ranges, affected API/env/source/permission contracts, verification, and rollback notes.
- Backend logging evidence: logger config, request/trace id middleware, structured fields, redaction list, safe examples, request/auth/validation/query/cache/pool/export/error log points, slow-query/report thresholds, sampling/retention, and error-envelope correlation.
- Deployment/config notes, observability notes, pagination/performance limits, concurrency/thread/worker model, Redis/cache notes, database/upstream/cache connection-pool notes including `ApiError`/timeout/exception cleanup and pool max such as `STARROCKS_POOL_MAX`, async/offline job contract for long-running work, timeout/retry/circuit-breaker/fallback behavior, rate/concurrency limits, proof that global filters/sort/page/aggregation are pushed to the source/provider/repository instead of full-materialize-then-filter, SQL query-writing evidence for risky database-backed endpoints, SQLite fixture/source-mode proof when simulation data is used, and rollback notes.
- Test/production profile evidence: `.env.test` and `.env.production`, loaded profile, backend/API base URL, source mode, auth/SSO endpoint, CORS allowlist, health/readiness path, and any sensitive values supplied through external secret channels.

For frontend integration:

- Frontend URL/build and loaded environment profile.
- Backend/API/provider base URL, source mode, auth/SSO behavior, and retained mock/offline status.
- Report data-visualization frontend evidence when applicable: user purpose, first-screen answer, component/chart choice, metric formatting/口径/freshness, filter/linkage/drill-through behavior, provider mapping, state coverage, performance controls, theme/accessibility, screenshots, and `VIS-*` findings or no-issue result.
- Runtime QA evidence: build/start command, browser URL, console/network check, interaction smoke, screenshot paths, visual regression/multimodal review status, and known blockers.
- Code file ledger proof for changed frontend/prototype files: ledger path, pre-change read/create status, appended version, component/config/API-client/style ranges, affected props/events/API/env/filter contracts, verification, and rollback notes.
- Testing handoff: page/module behavior, filters, interactions, permissions, export/download, edge states, accounts/data, and retest criteria.

For testing integration:

- Test case matrix, execution result, environment profile (`test` or `production`), config file loaded (`.env.test` or `.env.production`), version/account, frontend/backend URLs, golden/baseline dataset, metric/model/API/frontend/export reconciliation evidence, permission/cache/export/performance/exception/UAT/smoke/regression coverage, evidence, and defect list.
- Retest loop status: open/fixed/retest/closed/blocked for every blocker/major defect.
- Final readiness: pass, partial pass, fail, or blocked with exact production risk.

## Defect Retest Loop

Every blocker or major defect must move through:

1. `open`: evidence captured and owner assigned.
2. `fixed`: owner reports a fix with changed artifact/version.
3. `retest`: tester reruns the exact retest criteria.
4. `closed`: expected result verified with evidence.
5. `blocked`: retest cannot run due to named missing URL/account/data/env/permission.

Do not close a defect from a statement alone; closure needs retest evidence.
