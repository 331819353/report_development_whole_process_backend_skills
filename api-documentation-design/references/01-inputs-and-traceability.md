# Inputs And Traceability

Use this reference when deciding what the API document is based on and how endpoint behavior traces to evidence.

## Input Types

- API inventory: endpoint id, module, method/path, purpose, request params, response model, priority, status, and pending notes.
- Requirements: user stories, page needs, reporting metrics, workflow actions, acceptance criteria, permissions, and delivery scope.
- Existing implementation: routes/controllers, schemas/DTOs, serializers, service methods, repositories, tests, and sample responses.
- Interface artifacts: OpenAPI fragments, Postman collections, frontend API clients, mock data, SQLite fixture notes, JSON response examples, integration notes, and previous API docs.
- Model/source artifacts: source models, logical models, response/view models, database tables/views, upstream APIs, field dictionaries, formulas, relationships, refresh cadence, and quality rules.
- Environment and policy artifacts: `.env.test`/`.env.production` profile notes, base URL, deployment environments, auth/SSO rules, common headers, CORS/proxy requirements, error standards, report data-service backend constraints, performance/resilience constraints, async/offline job constraints, SQL query strategy notes, and export limits.

## Authority Rules

- Prefer implemented behavior only when the task is documenting current implementation.
- Prefer API inventory or explicit product/backend contract when the task is designing future APIs.
- Prefer frontend display/mock contracts when the task is integration handoff and no backend contract has been finalized.
- Treat absent details as pending information. Treat contradictory details as `ENTRY-*` conflicts using `$quality-gate-validation`; unresolved `P0`/`P1` conflicts keep affected endpoint behavior `partial` or `blocked` and require user confirmation only before the affected endpoint behavior is repaired or documented as final.
- Treat complete but unreasonable endpoint design as a `DESIGN-*` finding using `$quality-gate-validation`. Examples include response grain that cannot support the component, filters that cannot drive data, endpoint grouping that mixes incompatible permissions/freshness, or examples that cannot prove the business flow.

## Traceability Rules

- Every endpoint should trace to a module/page/resource/service boundary.
- Every response schema should trace to a response model, DTO, serializer, implementation sample, or explicit designed contract.
- Every response field should trace to a source field, formula, transformation rule, upstream field, route-level constant, or unresolved item.
- Every request filter should trace to a supported query condition, business rule, frontend control, or documented unsupported behavior.
- Every auth/permission rule should trace to a policy, middleware, gateway rule, or pending confirmation item.

## Pending Item Triggers

Record a pending item when any of these are unclear:

- Source table, file, upstream API, or authoritative system.
- Field name, type, nullability, unit, precision, enum dictionary, ID semantics, or date format.
- Formula, denominator, aggregation grain, sorting, Top/Bottom rule, fiscal calendar, or rounding rule.
- Required request param, default filter, pagination default/max limit, stable sort, export behavior, async job lifecycle, upload/download shape, or error code.
- Report data-service backend decisions such as report metadata source, report type, dimension/metric/filter/sort whitelist, backend-owned SQL/source mapping, parameter guardrails, permission injection, cache safety, result metadata, freshness/quality, audit, or slow-report governance.
- Auth header, token validation path, role/permission rule, environment profile value, CORS/proxy rule, health/readiness behavior, logging/request ID/observability expectation, timeout, retry, cache behavior, rollback path, or testing handoff evidence.
- Database-backed query decisions such as selected columns, sargable predicates, join keys/cardinality, dedup/order need, dynamic optional-filter handling, aggregation/window placement, or plan-evidence expectation.

Use `ENTRY-*` instead of a pending item when two artifacts provide incompatible confirmed-looking claims, such as different formulas, grains, field names, auth rules, endpoint ownership, or runtime behavior.

Use `DESIGN-*` instead of a pending item when facts are present but the proposed API/document structure is unreasonable for downstream implementation, frontend integration, or testing.
