# Contract Sources And Authority

Use this reference when collecting API contracts and deciding which artifact is authoritative.

## Contract Sources

- API documentation or OpenAPI schemas.
- Frontend clients, hooks, services, adapters, mock data, display code, and integration tests.
- Backend routes, controllers, schemas, DTOs, serializers, services, repositories, and tests.
- SQLite fixture databases, schema/seed files, JSON response examples, generated sample payloads, Postman collections, and curl examples.
- Runtime responses from local, staging, production-like, upstream, or database-backed environments.
- Product, security, permission, performance, and delivery requirements.

## Authority Selection

- If validating implemented behavior, compare runtime responses against the published contract and consumer expectations.
- If validating design before implementation, treat the approved API documentation or OpenAPI schema as authoritative.
- If replacing frontend mocks, treat the consumer-facing display contract as a required compatibility input until an adapter decision changes it.
- If validating backend/API implementation that uses simulated data, require SQLite fixtures as the local data-source authority. JSON files may document response examples but must not be treated as the implemented API source.
- If integrating upstream services, treat upstream response as source behavior but validate the local API response after transformation.
- If artifacts conflict, use `$quality-gate-validation` and record an `ENTRY-*` finding. Missing information is for absent facts; contradictory confirmed-looking facts need an authority decision. Unresolved `P0`/`P1` conflicts block pass status and require user confirmation unless an existing approved contract clearly resolves the authority.
- If artifacts agree but the selected API shape is unreasonable for the consumer, use `$quality-gate-validation` and record a `DESIGN-*` finding. Examples include a response grain that cannot support the UI, one endpoint mixing incompatible permissions/freshness needs, export behavior without a feasible source strategy, or auth behavior that cannot support expected user flows.

## Scope Statement

Start each validation by naming:

- Endpoint, operation, event, or query in scope.
- Consumer or downstream system.
- Source artifacts compared.
- Entry consistency status and relevant `ENTRY-*` findings, when contract sources disagree.
- Design reasonableness status and relevant `DESIGN-*` findings, when the contract shape affects consumer usability or testability.
- Runtime/source mode, such as mock contract, SQLite fixture, upstream, database, local service, staging, or production-like.
- Out-of-scope behavior, if any.
