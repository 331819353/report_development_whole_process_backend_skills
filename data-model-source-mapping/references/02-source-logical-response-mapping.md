# Source Logical Response Mapping

Use this reference when mapping raw data into business and API-facing models.

## Mapping Order

Always map in this order:

1. Business question, subject area, and consuming scenario.
2. Business process/object and intended analysis grain.
3. Source system and physical object.
4. Source model, layer, model type, and physical fields.
5. Logical/business model.
6. Response/view model.
7. Metric, additivity, and transformation rules.
8. Gap IDs for anything unresolved.

Do not jump directly from mock fields to response fields without checking source and logical models.
Do not jump directly from source tables to facts or summaries without naming the business process and grain.

## Source Model Rules

For each source model, state:

- Physical object name and source ID.
- Subject area and business process/object.
- Layer and model type, such as ODS source, DWD transaction fact, DIM dimension, DWS summary, ADS application table, bridge, or wide table.
- Business meaning.
- Grain, such as one row per order, project, product-day, organization-month, or alert event.
- Primary key or natural key.
- Business time field, ingestion/ETL time field when available, and date/partition field.
- Dimensions, measures, enums, and nullable fields.
- Additivity for measure fields when known.
- Update mode: full, incremental, zipper/SCD, snapshot, event, or unknown.
- Owner, refresh cadence, permission, and known quality risks.

If grain, key, owner, or refresh cadence is unknown, create a `GAP-*` item.

## Logical Model Rules

Logical models should represent business objects, not screens. Good examples:

- Organization.
- Product.
- Customer.
- Order.
- Contract.
- Payment.
- Inventory snapshot.
- Project.
- Alert.
- Task.
- Period summary.
- Bridge or relationship model for many-to-many relationships.

For each logical model, define:

- Subject area and business process/object.
- Source models used.
- Grain after joins or aggregation.
- Keys and relationship cardinality.
- Whether historical, snapshot, or event data is required.
- Layering choice: DWD detail, DIM conformed dimension, DWS reusable summary, ADS application model, or accepted simplification.
- Whether the model is a transaction fact, periodic snapshot fact, accumulating snapshot fact, factless fact, dimension, bridge, summary, wide, or application model.
- Whether summary or wide-table materialization is justified by a repeated query pattern, governed metric reuse, export need, or high-frequency page/API.
- How many-to-many relationships avoid duplicated measures: bridge table, allocation, pre-aggregation, or explicit non-support.
- Permission boundary, such as user org scope, region scope, project scope, or role scope.

## Response/View Model Rules

Response/view models should represent API/frontend shapes. They may be page-specific when the shape is genuinely page-specific.

For each response field:

- Map to a source field, logical field, metric ID, static enum, or `GAP-*`.
- State type, unit, precision, enum label, null rule, and example.
- State sensitivity, masking rule, and field-level permission when the field can expose customer, employee, financial, operational-risk, or commercially sensitive data.
- Mark calculated fields explicitly.
- Keep display labels separate from field names.

Response/view models may consume ADS or DWS when the API/page needs precomputed metrics, high-frequency query speed, or page-specific layout fields. Document the traceability path back to DWS/DWD/ODS or the accepted source.

## Layering And Serving Rules

- ODS/source-aligned objects are for traceability and replay, not governed reporting by default.
- DWD facts should be process-based, single-grain, cleaned, deduplicated, and traceable.
- DIM models should be conformed and hierarchy/history aware.
- DWS summaries should hold reusable governed metrics at common grains.
- ADS/application models should serve concrete dashboards, APIs, exports, and high-frequency views; they may denormalize but must remain traceable.
- Do not put all logic in ADS when a metric is shared by multiple reports. Promote shared口径 to DWS.
- Do not create an all-purpose super-wide table. Wide models need a subject/application boundary and field blocks.

## Historical And Many-To-Many Rules

- If analysis needs state at event time, record the historical attribute on the fact or join to a SCD/zipper dimension by effective time.
- If only current value matters, document Type 1/current-state behavior.
- For many-to-many, use bridge/relationship models. Do not store comma-separated IDs as the analytic relationship.
- When a bridge can multiply measures, document allocation, pre-aggregation, or restricted metric support.

## Stable Field Naming

Use stable lower camel case for response fields unless the project already has a convention.

Examples:

- `period`
- `orgId`
- `orgName`
- `metricValue`
- `targetValue`
- `completionRate`
- `momRate`
- `yoyRate`
- `riskLevel`
- `ownerName`

Do not mix Chinese field names and English field names in the same response model unless the existing prototype/API contract already does so.

## Source Replacement Compatibility

When a source table, upstream API, fixture schema, or serving model changes, the response/view model remains the consumer-facing contract.

For each affected response model, add or update a compatibility mapping:

| Response field | Old source/formula | New source/formula | Transform/default/null rule | Behavior stable? | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |

Rules:

- Keep existing response field codes, casing, nesting, types, units, precision, enum meanings, nullability, formulas, grain, and empty/no-permission behavior unchanged.
- Do not rename response fields to match new source columns. Use source aliases or adapter mapping.
- New fields must be additive, named by the project convention, and documented with source trace, business meaning, type, unit, precision, nullability, sensitivity/permission, and compatibility status.
- If a response field cannot be produced by the new source, create a `GAP-*` item and keep the affected model `partial` or `blocked`.
- If the business intentionally changes a response field, mark it as a breaking model/API change and route to API documentation, change-impact analysis, and contract validation.

## Blank Cell Rule

For model tables, fill non-applicable cells with `none` and unknown cells with `TBD(GAP-*)`. Do not leave blanks for type, unit, precision, null rule, sensitivity, mapping, permission, owner, refresh cadence, or status.
