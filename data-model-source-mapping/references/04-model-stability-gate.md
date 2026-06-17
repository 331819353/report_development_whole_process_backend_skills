# Model Stability Gate

Use this gate before finalizing a 数据模型文件.

## Required Traceability

Every row must be traceable:

- Business question -> subject area, business process/object, metric/dimension needs, or gap ID.
- Model -> layer, model type, grain, key, owner, refresh cadence, and status.
- Response field -> source field, logical field, metric ID, static enum, or gap ID.
- Metric -> source fields, formula, additivity, numerator/denominator where needed, grain, dimensions, period logic, business time field, or gap ID.
- Logical model -> source model, layer/type, grain, and relationship rule, or gap ID.
- Data quality rule -> model/field target.
- Permission rule -> identity scope and data scope, or gap ID.
- Sensitive field -> sensitivity value, masking rule, field-level permission, or gap ID.
- Summary/wide/ADS model -> query pattern, reuse/application reason, traceability path, or gap ID.

## No-Invention Checks

Create a gap instead of inventing:

- Table/view/file/API physical names.
- Field names that do not appear in source docs or prototype code.
- Join keys.
- Grain and business time口径.
- Subject area, business process, or model layer/type.
- Additivity and numerator/denominator rules.
- Formula components.
- Enum dictionaries.
- SCD/history behavior.
- Many-to-many allocation or bridge behavior.
- Late-arriving/backfill and deduplication rules.
- Owner names.
- Refresh cadence.
- Permission rule details.
- Sample values presented as real source data.
- Sensitivity level, masking behavior, or field-level permission.

## Stable Output Checks

- Use IDs: `SRC-*`, `LGM-*`, `RSP-*`, `MET-*`, `GAP-*`.
- Use status values: `ready`, `partial`, `blocked`.
- Put `Gap IDs` in a dedicated column where uncertainty exists.
- State one grain per fact/logical/summary/response model.
- Keep layer and model type explicit: ODS, DWD, DIM, DWS, ADS; fact, dimension, bridge, summary, wide, application.
- Avoid duplicate response field definitions across models unless the models intentionally differ.
- Preserve existing response field names, casing, nesting, type, unit, precision, enum meaning, nullability, formula, grain, and empty/no-permission behavior when a source table/upstream/fixture changes.
- Add new response fields only as additive, conventionally named fields with source trace, type, unit, nullability, sensitivity/permission, and compatibility status.
- Use the same model names later in API清单.
- Do not leave required table cells blank. Use `none` when intentionally not applicable, or `TBD(GAP-*)` when unknown.
- A row with `TBD(GAP-*)` cannot be `ready`.

## Priority Note

If API priorities exist, use `P0/P1/P2` from the API清单. If no API清单 exists yet, treat first-screen, required response, core metric, permission, source, and join items as `core/required` for readiness decisions.

## Readiness Decision

Mark the model file:

- `ready`: all P0 or core/required business questions, subject areas, processes, grains, source mappings, joins, core metrics/additivity, response fields, permissions, security rules, layer decisions, and quality rules are confirmed.
- `partial`: assumptions exist but are documented and do not block API documentation.
- `blocked`: unknown formula, source, business process, grain, layer/type, join, metric additivity, history/SCD, many-to-many rule, permission, security rule, or quality rule prevents reliable API documentation.

## Model Design Red Flags

- A model/table is created before business question, subject area, business process/object, and grain are defined.
- A source/table/upstream replacement changes response field codes or behavior instead of updating mapping/adapter rules.
- New source columns are exposed as API/response fields without naming convention, source trace, type/unit/nullability, or permission review.
- One table/model mixes multiple grains without a bridge or summary strategy.
- The model mirrors source-system tables directly for governed reporting without DWD/DIM/DWS/ADS reasoning.
- A shared metric is recalculated separately in multiple ADS/report models instead of being governed in a reusable layer.
- A ratio, rate, average, unit price, retention, or conversion metric is stored without numerator/denominator.
- Semi-additive snapshot metrics such as inventory or balance are summed across time without a rule.
- Many-to-many relationships are stored as comma-separated IDs.
- Historical reports depend on current-only dimensions when event-time state matters.
- A super-wide table mixes unrelated domains or unmanaged field blocks.
- Summary models include too many dimensions and risk sparse row explosion.
- Quality rules, lineage, freshness, or owner are missing for core models.
