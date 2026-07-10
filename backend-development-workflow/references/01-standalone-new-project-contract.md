# Standalone Backend New-Project Contract

Use this contract when the user asks for backend/API/data-service development and there is no prototype, executable prototype PRD, or configured prototype project. Prototype artifacts are not required for this mode.

## Entry Decision

Set `backendEntryMode = standalone-new-project` when all are true:

- The requested deliverable is a real backend service, API, or data service.
- No existing backend project is the writable target.
- No prototype handoff is available or the user explicitly wants development without one.

Do not route to prototype generation. Build the backend from requirements, source evidence, API expectations, security/environment constraints, and the selected engineering stack.

## Minimum Inputs

Start from the best available combination of:

- User goal, consumers, use cases, functional scope, business rules, acceptance wording, and hard constraints.
- API expectations, source systems/tables/views/upstream APIs, representative data, field meanings, filters, permissions, auth/SSO, environment, deployment, and non-functional requirements when available.
- Required language/framework or repository conventions when specified.

Missing optional material does not block project scaffolding. Missing facts that affect endpoint correctness, source queries, permissions, or production readiness become `GAP-BE-*` with an owner and closure condition.

## Stack Selection

- Preserve a user-specified or repository-authoritative stack.
- Use `$python-flask-sso-multidatabase-backend` for Python/Flask work or when the user accepts the bundle default.
- Use `$java-springboot-backend-development` for Java/Spring Boot work.
- If no stack is specified and implementation is requested, choose the bundle's Python + Flask + SQLAlchemy baseline and record the decision in `standaloneBackendBaseline`.

## Required Planning Artifacts

| Artifact | Required contents |
| --- | --- |
| `standaloneBackendBaseline` | Goal, writable root, consumers, stack/overrides, runtime/deployment target, auth, source availability, NFRs, assumptions/gaps. |
| `serviceBoundaryMatrix` | Module/use case, route/API family, service owner, repository/source owner, auth/permission, transaction/runtime boundary, status. |
| `apiContractMatrix` | Method/path, consumer, request params/body, response fields/envelope, errors, auth, pagination/sort, versioning, verification. |
| `sourceObjectUnderstandingMatrix` | Source object, representative content, grain, keys, fields, filters, permission fields, bounds, nulls, freshness, evidence/gap. |
| `requestParamPredicateMatrix` | Request parameter, validation/default, source field/operator, permission injection, order/page impact, test evidence. |
| `implementationVerificationMatrix` | API/use case, code path, unit/integration/contract/runtime evidence, error/permission case, status/gap. |

## Minimal Interface Boundary

The minimal-interface principles apply whether or not a prototype exists:

- Inspect every involved table/view/fixture/upstream object before endpoint implementation.
- Client-visible filters are request parameters mapped to source predicates.
- Simple retrieval is projection + predicates + permission scope + stable order + bounded pagination.
- Do not add hidden joins, aggregation, totals, exact counts, rankings, formulas, chart/KPI derivation, broad in-memory filtering, or response reshaping.
- Derived behavior requires an explicit design, governed model/view/precompute source, or `GAP-BE-DERIVED-*`.

If the real source is unavailable, do not invent production table semantics. You may initialize project structure, API contracts, migrations/schema placeholders, and test fixtures, but keep source-dependent endpoints `partial` or `blocked` until representative source content is understood.

## Workflow

1. Resolve the writable backend root and `backendEntryMode`.
2. Inspect requirements, consumer expectations, available source content, auth/env/deployment constraints, and workspace conventions.
3. Select the stack and initialize the real backend project when no target exists.
4. Establish configuration profiles, application entrypoint, health/readiness, response/error envelope, request/trace IDs, logging/redaction, auth middleware/filter, and test structure.
5. Define `serviceBoundaryMatrix` and `apiContractMatrix` before broad route implementation.
6. For every data-bearing endpoint, complete source understanding and request-param predicate mapping before repository/mapper code.
7. Implement one vertical slice first: route/controller -> validation/auth -> service -> repository/source adapter -> schema/DTO -> error handling -> tests -> runtime smoke.
8. Expand by use case while preserving thin controllers, explicit transactions, resource cleanup, source-aligned queries, and stable contracts.
9. Configure pools/timeouts, Redis only when justified, environment/secrets, migration/seed strategy, observability, deployment, and rollback.
10. Run formatting/static checks, unit/integration/contract tests, build/package, startup, health/API smoke, permission/error cases, and connection cleanup checks.
11. Produce API docs, source/contract evidence, changed files, commands, URL or blocker, gaps, and readiness.

## Readiness

- `ready`: requested backend scope is implemented and runnable with verified contracts, source behavior, auth/error handling, tests, and runtime evidence.
- `partial`: service structure and bounded functionality run, but source/auth/environment/deployment or production evidence remains incomplete.
- `blocked`: an essential source/business/security decision prevents a correct bounded implementation.

Prototype absence by itself is never a blocker in this mode.

## Required Output

- `backendEntryMode = standalone-new-project`
- `standaloneBackendBaseline`
- `serviceBoundaryMatrix`
- `apiContractMatrix`
- `sourceObjectUnderstandingMatrix`
- `requestParamPredicateMatrix`
- `implementationVerificationMatrix`
- Project path, changed files, commands, tests/build results, runtime URL or blocker
- Open `GAP-BE-*` with owner and closure condition
- Final `ready`, `partial`, or `blocked`

