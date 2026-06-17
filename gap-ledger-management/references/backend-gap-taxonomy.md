# Gap Taxonomy

Use this reference to classify missing or assumed backend/API information.

## Categories

- Data source gaps: missing files/tables/views, upstream endpoints, malformed rows, authoritative source, refresh cadence, ownership, credentials, sample rows, and join keys.
- Data model gaps: missing fields, unknown types, nullable rules, IDs, primary keys, enum dictionaries, units, precision, uniqueness, relationship cardinality, and retention rules.
- Transformation gaps: date/period conversion, aggregation grain, formulas, denominator rules, unit conversion, rounding, default fill, sorting/grouping, Top/Bottom logic, and reconciliation.
- API contract gaps: endpoints, params, pagination, sorting, filters, response examples, error behavior, upload/download, idempotency, compatibility, and consumer expectations.
- Auth/config/deployment gaps: auth headers, token rules, SSO values, environment variables, ports, CORS/proxy, credentials, network access, secrets, deployment target values, startup commands, health/readiness endpoints, and rollback/restore paths.
- Observability/reliability gaps: log format, request ID, trace/metric availability, alert owner, timeout/retry behavior, upstream failure handling, health check coverage, and SLA/SLO expectations.
- Integration/upstream gaps: upstream availability, request limits, timeout/retry, response variability, versioning, ownership, fallback rules, and SLA.
- Testing/evidence gaps: unavailable test data, missing fixtures, untested branches, no runtime URL, missing auth token, skipped tests, flaky evidence, missing retest criteria, or absent retest evidence.
- Performance gaps: page limits, export limits, cache/precompute, timeout, retry, large-data handling, expensive filters, and concurrency expectations.
- Business definition gaps: metric definitions, formulas, ownership, permission scope, status rules, process state, approval rules, and acceptance criteria.

## Severity

- `P0 blocked`: implementation or integration cannot proceed reliably.
- `P1 risky`: work can proceed with a temporary assumption but may cause rework or user-visible errors.
- `P2 clarify`: useful confirmation needed, but current behavior is low risk.
- `P3 note`: documented context or future cleanup.

## Status

- `open`: unresolved.
- `assumed`: temporary behavior is in use and must be confirmed.
- `confirmed`: decision received but affected artifacts may still need updates.
- `resolved`: decision applied to code/docs/tests.
- `wontfix`: explicitly accepted as out of scope.
