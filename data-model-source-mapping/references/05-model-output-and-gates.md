# Data Model Output And Gates

## Hard Constraints

- Every response/view field must trace to a source field, formula, static enum, or `GAP-*` item.
- Every metric-bearing response/view field must define value type, raw/display unit, display scale, screen precision, tooltip/export precision, rounding mode, null/zero/denominator-zero behavior, negative-zero handling, small-nonzero behavior when relevant, formula precision policy, and formatter ownership.
- Response/view field names, nesting, types, units, precision, enum meanings, nullability, formulas, grain, and empty/no-permission behavior are stable compatibility contracts across source/table replacement. Source names may change; response contracts may not drift silently.
- New response/view fields must follow the project naming convention, or stable English lowerCamel when no convention exists, and must declare source, meaning, type, unit, nullability, permission/sensitivity, compatibility status, and downstream consumers.
- Do not resolve contradictory source/model/API/frontend evidence by preference or convenience; unresolved `P0`/`P1` conflicts keep affected models `partial` or `blocked`.
- Every metric must have formula, grain, dimensions, period logic, source dependency, precision, and numeric display contract, or a `GAP-*` item.
- Snapshot/latest-period response models must trace to source/logical/precompute/cache/snapshot models through explicit data-version fields and source/filter predicates. Do not define one response model as the authoritative source for another response model unless it is explicitly modeled as a canonical/shared snapshot with grain, fields, scope, and reuse rules.
- Filterable response/view models must prove data completeness before filter binding: option dimensions, matching fact/business rows, required fields, default/non-default states, empty/no-permission states when relevant, and resolver/API branch coverage. Missing evidence is a `GAP-*`, not a frontend binding assumption.
- Source ownership, refresh cadence, and permission must be explicit, assumed, or blocked.
- Joins and hierarchy rollups must be documented before API documentation starts.
- Prototype mock fields must be reconciled with real source fields instead of copied blindly.
- Do not keep a model structure that is technically traceable but unreasonable for the consuming API/UI/test workflow. Use `DESIGN-*` findings when grain, joins, response shape, metric formula, transformation, permission, or freshness design would distort the business answer.
- Do not use a field in a response model if its type, unit, enum, or null behavior is unknown and undocumented.
- Sensitive fields must declare sensitivity level, masking rule, and field-level permission behavior, or link to `GAP-*`.
- Do not leave required table cells blank. Use `none` when intentionally not applicable, or `TBD(GAP-*)` when unknown.


## Required Output

Use this structure for the 数据模型文件:

1. Model overview: purpose, supported pages/APIs, owner, status.
2. Data sources: source name, type, location, owner, refresh, permission, reliability notes.
3. Source models: physical fields and metadata.
4. Logical models: business objects, keys, relationships, grain, joins.
5. Response/view models: API/frontend fields, types, units, numeric display contracts, null rules, examples.
5a. Source replacement compatibility: old source, new source, unchanged response fields, additive fields, transform/default/null rules, and breaking/versioning decisions.
6. Data-version/snapshot semantics: snapshot role, business time, snapshotDate/latestPeriod, loadBatch, dataVersion, freshness, invalidation/backfill, exposing response metadata, source fields/partitions, filter predicate mapping, and reuse rules when canonical/shared.
7. Filter-support completeness: option source, row grain, fields, default/non-default states, empty/permission states, resolver/API branches.
8. Metrics: formulas, dimensions, baselines, thresholds, numeric display contracts, reconciliation.
9. Transformation mapping: source -> logical -> response.
10. Security rules: sensitivity, masking, field-level permission, no-permission behavior.
11. Data-quality rules: uniqueness, completeness, enum validation, range checks, freshness.
12. Pending model items: linked `GAP-*` IDs or summary.
13. Design reasonableness status: linked `DESIGN-*` IDs, repairs, or accepted limitations.


## Quick Quality Gate

- Every response/view field traces to a source field, formula, or pending item.
- Existing response/view contracts remain stable when source tables or data sources change; any drift is blocked unless explicitly versioned.
- Additive fields are named and documented by convention before downstream API/front-end/test use.
- Every metric in the indicator list has formula, grain, dimensions, source dependency, and numeric display contract.
- Data-version and snapshot semantics are explicit when current/latest/snapshot endpoints exist.
- Data-version and scope params map to source fields, partitions, logical filters, precompute keys, or cache keys before response/view models are declared ready.
- Filter-support completeness is documented before downstream `filterFields`, query params, or resolver params are accepted.
- Source ownership, refresh cadence, and permission are explicit.
- Model IDs and API response model names are stable for downstream API inventory, documentation, frontend integration, and testing artifacts.
- Model design reasonableness is checked; unresolved `P0`/`P1` `DESIGN-*` findings keep affected models `partial` or `blocked`.
- All unresolved model issues are visible in the pending model items section with `GAP-*` IDs.
