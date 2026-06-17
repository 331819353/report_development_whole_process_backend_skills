# Metrics Transformations Quality

Use this reference for metric口径, transformations, permissions, and data quality.

## Metric Formula Requirements

Each metric needs:

- Metric ID and name.
- Metric type: atomic, derived, or composite.
- Formula in business words.
- Numerator and denominator, when applicable.
- Additivity: additive, semi-additive, or non-additive.
- Aggregation grain.
- Supported dimensions.
- Time口径 and business time field.
- Period logic: day, week, month, quarter, year, rolling period, MTD, QTD, YTD, custom.
- Filter/scope conditions.
- Deduplication rule.
- Baseline and threshold.
- Direction: higher-is-better, lower-is-better, neutral, or range.
- Unit and precision.
- Source dependency.
- Reconciliation rule or comparison source.
- Owner and refresh frequency when the metric is shared across reports.

If a formula says only "按业务口径计算", create a `GAP-*` item.

## Metric Type And Additivity Rules

- Atomic metrics are base measures that should not be decomposed further for the current model, such as pay amount, order count, refund amount, exposure count, or click count.
- Derived metrics add scope, period, segment, or filter to atomic metrics, such as 7-day pay amount, app-channel pay amount, or new-customer order count.
- Composite metrics are calculated from other metrics, such as conversion rate, refund rate, customer unit price, retention rate, or completion rate.
- Additive metrics can be summed across aligned grains and normal dimensions.
- Semi-additive metrics, such as inventory, balance, assets, or headcount snapshots, need a time aggregation rule such as end-of-period, average, min, or max.
- Non-additive metrics, such as rates, ratios, averages, unit prices, and retention, must not be summed. Store numerator and denominator so upper layers can recompute totals.
- Do not let several metrics share a vague name such as "sales amount" when their source, time口径, refund/tax/freight handling, or filter scope differs.

## Transformation Rules

Document transformations explicitly:

| Transformation type | Required detail |
| --- | --- |
| Date conversion | Source timezone, output format, period boundary |
| Period aggregation | Grouping field, period type, partial-period behavior |
| Unit conversion | Source unit, output unit, scale, rounding |
| Enum mapping | Source values, display labels, unknown handling |
| Hierarchy rollup | Parent key, rollup rule, missing parent handling |
| Deduplication | Dedup key, order rule, duplicate handling |
| Default fill | Fill value, affected fields, whether shown to users |
| Permission filtering | User scope, org/project/region rule, no-permission behavior |
| Late-arriving/backfill | Business time, load time, replay window, overwrite/upsert rule |
| SCD/history matching | Effective start/end fields, event-time match rule, current vs historical behavior |
| Many-to-many handling | Bridge model, allocation rule, pre-aggregation, duplicated-measure prevention |
| Additivity handling | Numerator/denominator preservation, semi-additive time rule, non-additive recomputation |

## Data Quality Rules

Use these rule types:

- `uniqueness`: primary key or natural key uniqueness.
- `completeness`: required fields not null.
- `enum-validation`: values belong to allowed dictionary.
- `range-check`: numeric/date values in valid range.
- `freshness`: refresh time within allowed SLA.
- `referential-integrity`: join keys match parent/child models.
- `reconciliation`: totals match trusted source or known tolerance.
- `dimension-hit-rate`: fact keys match conformed dimensions above the accepted threshold.
- `metric-fluctuation`: core metric volume/value change stays within expected range or alerts.
- `deduplication`: duplicate event/business keys are removed according to the model rule.
- `backfill-readiness`: late-arriving/replayed data updates affected layers correctly.

Severity:

- `Blocker`: invalidates core metric or source traceability.
- `High`: can show wrong business result, permission leak, or misleading trend.
- `Medium`: affects secondary filters, examples, or edge cases.
- `Low`: naming, copy, or non-blocking metadata.

## Permission Rules

Permission cannot be a vague note. State:

- Auth source or identity type.
- User scope field.
- Data scope field.
- Whether scope is inherited from org, project, region, product, or role.
- No-permission behavior: empty result, masked field, error, or hidden API.
- Field-level sensitivity and masking rule for sensitive fields.

If permission is unknown, link a `GAP-*` item and do not mark affected APIs/models `ready`.

## Naming And Null Rules

- Field names must carry business meaning. Avoid vague names such as `amount`, `money`, `num`, `type`, `status`, `flag`, or `time` when a clearer name is possible.
- Amount fields should state semantics, such as `origin_amount`, `discount_amount`, `coupon_amount`, `freight_amount`, `pay_amount`, `refund_amount`, or `net_amount`.
- Time fields should state business event, such as `order_create_time`, `pay_success_time`, `refund_time`, `finish_time`, `etl_time`, or `dt`.
- Boolean fields should follow one convention, such as `is_new_user`, `is_member`, `is_deleted`, or `is_valid`.
- Unknown dimension members should use one consistent rule, such as unknown key plus unknown label. Do not mix `NULL`, `0`, `-1`, and `unknown` across models without documentation.
- Distinguish unknown from truly zero. Detail-layer nulls may preserve source meaning; summary-layer amounts/counts often fill with 0 when business-approved.

## Security And Masking Rules

For sensitive fields, document:

- Sensitivity: `public`, `internal`, `confidential`, `sensitive`, or `unknown`.
- Whether the field can be returned through APIs.
- Whether the field is masked, hidden, aggregated, or role-limited.
- Masking format, such as partial phone, partial name, hidden amount, bucketed value, or `TBD(GAP-*)`.
- Whether export behavior differs from screen display.

If sensitivity is unknown, create a `data-security` gap.
