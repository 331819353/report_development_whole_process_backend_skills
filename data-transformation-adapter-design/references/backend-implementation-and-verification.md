# Implementation And Verification

Use this reference when translating transformation rules into code, tests, and examples.

## Placement Rules

- Put raw file/database/upstream parsing in repository, data-access, client, or adapter code.
- Put source-to-target conversion, aggregation, and business formulas in service or transformation modules.
- When the authoritative source is a database, push eligible filtering, sorting, pagination, joins, grouping, aggregation, Top/Bottom, and count calculations into SQL/database views/repository queries. Do not pull broad database rows into memory for business filtering or aggregation.
- Do not use a full-materialize-then-filter pipeline for global/page-level scope. Source/repository code must apply global request filters, permission scope, sorting, pagination, ranking, and aggregation before service-layer response shaping. Building a complete target list and trimming it later is a fail unless the input is a documented component-internal filter over already fetched component data, tiny static enum, or bounded lookup.
- When API implementation uses mock data, model the mock source as a SQLite fixture database and query it through the repository/data-access layer. Do not use JSON files, Python/JS arrays, or in-memory collections as the transformation source for backend/API simulation.
- SQLite simulation must be experience-equivalent to the real API for parameter behavior. Seed fewer rows if necessary, but include enough combinations for filters, date ranges, dimensions, statuses, permissions, sorting, pagination, Top/Bottom, drilldown, empty, abnormal, and aggregate scenarios to produce visibly different responses.
- When real database table/view metadata is available, implement the source-to-response mapping through SQL, views, repository queries, or bounded service transformations. After contract, field quality, permission, performance, and verification checks pass, the real SQL-backed path can be published directly and must become the default source.
- When replacing a source table/upstream/fixture, keep the target API response contract stable. Existing fields keep their names, nesting, types, units, precision, enum meanings, nullability, formulas, grain, and empty/no-permission behavior; source changes are handled through SQL aliases, repository mapping, DTO serializers, or adapters.
- Newly available source columns stay internal unless intentionally added as additive response fields with project-convention names, source trace, type/unit/nullability, sensitivity/permission, and compatibility status.
- Keep service-layer transformations for bounded response shaping: field renames, enum labels, unit/precision formatting, DTO assembly, and small confirmed post-processing.
- Put final response validation in schemas, DTOs, serializers, response helpers, or contract tests.
- Keep transformations deterministic and documented.
- Do not hide business formulas or source-specific cleanup inside route handlers.
- Preserve raw values only when the target contract explicitly needs them.

## Verification Sample Template

- Scenario:
- Request params:
- Source rows or upstream payload:
- SQLite fixture table/query when simulation is used:
- Real table/view query when authoritative source is used:
- Transformation rules exercised:
- Parameter changes exercised:
- Source quality cases:
- Expected response fields:
- Source replacement compatibility: old source -> new source mapping, preserved response fields, additive fields, breaking/versioning decisions:
- Reconciliation notes:
- Status: pass / partial / fail

## Test Guidance

- Add focused tests for non-trivial field renames, date/period conversion, aggregation, formulas, enum mapping, unit conversion, rounding, default fill, sorting, and empty states.
- For SQLite simulation, add parameter-variation tests proving that filters, time ranges, dimensions, permission scope, sorting, pagination, drilldown, and aggregate requests change the response according to the API contract.
- For real table-backed APIs, add mapping tests or SQL review samples proving that source table/view fields produce the prototype/API response fields and that the real source is the default publishable path after validation.
- For source/table/upstream replacement, add contract tests comparing the new source-backed response to the existing API schema or golden sample. Fail or mark partial on renamed, removed, moved, retyped, rescaled, re-enumed, re-nullable, re-formulated, or re-grained existing fields unless versioned migration is approved.
- Add source quality tests for missing keys, duplicate rows, malformed values, invalid enums, invalid dates, late-arriving data, and reject/quarantine behavior when those risks exist.
- Include at least one negative or missing-data sample when the rule has fallback behavior.
- Compare representative runtime responses against the target API contract when implementation exists, and record field/request/error mismatches with reproducible evidence.
- Record unknown rules or temporary defaults in a local transformation gap ledger with stable `GAP-*` IDs, owner, impact, assumption, and retest criteria.
- For database-backed transformations, include at least one test or review sample proving global request filters map to index-friendly SQL predicates. Reject or mark partial any implementation that depends on `FUNCTION(field) = ?`, date extraction on indexed date columns, arithmetic on indexed columns, unbounded leading-wildcard search, global full-materialize-then-filter behavior, or broad in-memory aggregation without an explicit indexed/generated/full-text/precompute strategy.
- For collection/list/table transformations, include pagination boundary tests for default page size, maximum page size, out-of-range pages, stable ordering, and total-count behavior.
