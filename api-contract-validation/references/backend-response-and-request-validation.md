# Response And Request Validation

Use this reference for detailed contract checks.

## Response Checks

- Required and optional fields.
- Field names, casing, aliases, and deprecated fields.
- Object/array nesting and item shape.
- Types, nullability, default values, units, precision, rounding, and enum values.
- Date/time/period format, timezone, fiscal/calendar assumptions, and sorting order.
- Empty-state shape, no-data shape, no-permission-scoped shape, and omitted-field behavior.
- Derived fields, aggregation values, totals, subtotals, and reconciliation with detail rows.

## Source Replacement Compatibility Checks

Run these checks whenever backend implementation changes the data source, source table/view, upstream API, SQLite fixture schema, precompute table, or serving model:

- Compare the new response against the previous API document, OpenAPI/schema, frontend adapter expectation, or golden runtime sample.
- Existing fields remain present and keep names, casing, nesting, types, units, precision, enum meanings, nullability, formulas, grain, ordering/export meaning, empty/no-permission behavior, and display semantics.
- New fields are additive, conventionally named, source-traced, typed, permission/sensitivity-reviewed, and optional/ignorable for existing consumers unless the contract explicitly versions a new required field.
- Renamed, removed, moved, retyped, rescaled, re-enumed, re-nullable, re-formulated, or re-grained fields are breaking findings unless a versioned migration and deprecation plan exists.
- The verification evidence includes at least one default sample and one affected non-default/filter or permission sample when the endpoint supports those states.

## Request Checks

- Path, query, header, and body parameter names.
- Required status, defaults, allowed values, multi-select behavior, and validation rules.
- Pagination names, defaults, maximums, total-count behavior, and out-of-range behavior.
- Stable default sort and cursor/keyset need for high-volume or deep-scroll result sets.
- Sorting syntax, default sort, allowed fields, stable ordering, and invalid sort behavior.
- Filter names, date-range inclusivity, timezone, hierarchy filters, search behavior, and permission-scoped defaults.
- For database-backed endpoints, each filter's source field, SQL predicate shape, and index support.
- Global/page-level filters and permission-scope filters must be visible as SQL `WHERE` predicates or equivalent source/provider query params; component-internal filters must be explicitly local to already fetched component data.
- Upload/download content types, filenames, streaming behavior, and export limits.

## Error And Auth Checks

- HTTP status and business code.
- Error envelope shape, message, detail, trace id, and recoverability.
- Invalid-param, unauthorized, token-expired, token-invalid, valid-token/no-permission, rate-limit, timeout, upstream failure, and data-source failure behavior.
- Whether sensitive values such as credentials, tokens, secrets, or raw upstream payloads are excluded from errors and logs.

## Performance Checks

- Default and maximum page size.
- Stable sort, total-count strategy, cursor/keyset need, and out-of-range page behavior.
- Export row/file limits.
- Timeout, retry, circuit-breaker, and fallback behavior.
- Cache/precompute assumptions and invalidation.
- Redis/cache assumptions when used: cache key dimensions, TTL, invalidation, permission/tenant safety, stampede protection, and fallback.
- Database connection-pool behavior for database-backed runtime: pooled connection reuse, max size, acquire timeout, idle timeout, validation/health behavior, and safe shutdown.
- Large result handling and known expensive filters or joins.
- SQL pushdown for database-backed endpoints: filtering, sorting, pagination, joins, grouping, aggregation, Top/Bottom, and counts should be performed by database queries rather than broad in-memory calculation.
- Flag page/API-level full-materialize-then-filter behavior when an implementation builds or loads a complete candidate dataset/component payload and then applies global filters, permission scope, sorting, pagination, ranking, grouping, aggregation, or counts. This is a fail/partial finding unless the behavior is a documented component-internal filter over already fetched component data, tiny static enum, or bounded lookup.
- Index-friendly predicates for filters and sorts. Flag `FUNCTION(field) = ?`, `DATE(field) = ?`, `YEAR(field) = ?`, `TO_CHAR(field) = ?`, `LOWER(field) = ?`, arithmetic on indexed columns, leading-wildcard search, or unknown index support as performance findings unless a matching function/generated/full-text index or precompute path is documented.
- Mock-derived backend/API implementations must query SQLite fixtures for local simulation. Flag JSON file reads, Python/JS arrays, or broad in-memory filtering as source/performance findings unless the user explicitly scoped the work outside backend/API implementation.
