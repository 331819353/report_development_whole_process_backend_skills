# Boundary And Mapping

Use this reference when defining the transformation boundary and field-level mapping.

## Boundary Definition

Name these items before writing rules:

- Target endpoint, operation, export, event, or adapter.
- Target consumer or contract.
- Authoritative source: file, database table/view, upstream API, event stream, fixture, or generated data.
- Source mode: SQLite simulation, real database table/view, upstream API, or other authoritative runtime source.
- Source grain: raw row, transaction, day, month, user, org, order, project, product, region, or other unit.
- Target grain: detail row, grouped row, KPI card, trend point, ranking item, tree node, export row, nested object, or summary.
- Transformation owner: repository, service, adapter, serializer, DTO, view, SQL, or upstream dependency.

## Field Mapping Template

For each target field, record:

- Target field:
- Source field(s):
- Source-to-target rule:
- Type:
- Required/nullability:
- Unit:
- Precision/rounding:
- Enum/date/format:
- Default-fill behavior:
- Error behavior:
- Source trace:
- Status: ready / partial / blocked

For prototype-derived contracts, the target field may come from mock/component data, but the source field must come from SQLite fixture schema or confirmed real table/view metadata. Do not treat a prototype mock field name as a real source field unless the source mapping confirms it.

## SQLite Fixture Quality Gate

Use this gate when SQLite simulates an interface built from prototype data structures:

- Every request parameter has matching and non-matching rows.
- Time, organization, region, product, customer, status, permission, drilldown, sorting, pagination, Top/Bottom, and empty-state behavior are represented when they exist in the API contract.
- Aggregates, totals, rankings, and derived metrics change when the relevant filter or dimension changes.
- Fixture data may be small, but it cannot be single-state or single-total data that makes every parameter return the same business answer.
- Unsupported parameter behavior is recorded as `partial` or `blocked`.

## Real Table Publish Gate

Use this gate when real table/view structure is available:

- Each target response field maps to a real source field, SQL expression, view column, formula, enum dictionary, permission rule, or explicit constant.
- If the real source replaces another source, existing target response fields stay stable. Confirm field name, nesting, type, unit, precision, enum meaning, nullability, formula, grain, and empty/no-permission behavior did not drift.
- Joins, grouping keys, period conversion, filters, sorting, pagination, and permission predicates can run in SQL/repository queries.
- Field quality, nullability, enum coverage, date format, unit, precision, and duplicate behavior are confirmed or captured as gaps.
- The real source path can replace SQLite as the default service source after contract, data quality, permission, and performance checks pass.

## Source Replacement Adapter Rules

Use these rules when old source and new source do not have the same physical fields:

- Freeze the target API contract before designing mappings.
- Map old-to-new at the field level: target field -> old source/formula -> new source/formula -> transform/default/null rule -> verification evidence.
- Prefer explicit SQL aliases, DTO serializers, and backend response adapters over changing response field names.
- Keep new source-only fields internal unless they are intentionally added as additive API fields with conventional names and documentation.
- Mark the adapter `blocked` when an existing required target field cannot be produced by the new source without an approved business default or formula.
- Mark the adapter `partial` when compatibility depends on a temporary default, changed null rule, incomplete enum mapping, or unverified sample.

## Source Quality Gate

Before finalizing field rules, check:

- Required source keys and join keys exist.
- Primary keys or grouping keys are unique when the target contract assumes uniqueness.
- Nullability and default-fill rules are known for required target fields.
- Malformed rows, invalid dates, invalid enum codes, negative values, and outliers have an explicit handling rule.
- Duplicate rows, late-arriving data, and source refresh cadence have an explicit reconciliation rule.
- Reject, quarantine, skip, or partial-success behavior is documented for rows that cannot be transformed.

## Missing Field Handling

- Mark a field blocked when no source, formula, default, or explicit constant can produce it.
- Mark a field partial when a temporary default or assumption is used.
- Do not invent a business formula only to satisfy the target contract.
- Record missing source fields, enum dictionaries, units, IDs, nullable rules, and precision in a local transformation gap ledger with stable `GAP-*` IDs, owner, impact, assumption, and blocking status.
