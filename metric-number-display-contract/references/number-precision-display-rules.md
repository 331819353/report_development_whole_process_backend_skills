# Number Precision And Display Rules

Use this reference when a report, component, API, frontend adapter, export, or QA gate touches numeric values, units, percentages, rates, rankings, money, scores, or any value that can be rounded.

## Core Principle

Numeric display is a governed contract, not a visual afterthought.

The required chain is:

```text
raw value -> calculation/aggregation with raw precision -> display scale/unit -> rounding mode -> screen label/table/chart/tooltip/export
```

Never round before aggregation, sorting, filtering, ranking, rate calculation, subtotal/grand-total calculation, export calculation, or reconciliation. Display precision cannot change the business value.

## Numeric Format Contract

Every implementation-ready metric-bearing component needs a numeric display contract for each visible measure.

| Field | Required meaning |
| --- | --- |
| `metricId` / `field` | Stable metric or response field code |
| `valueType` | `count`, `amount`, `currency`, `percent`, `rate`, `ratio`, `average`, `score`, `duration`, `rank`, `index`, `geo`, `scientific`, or project enum |
| `rawUnit` | Source unit, such as `yuan`, `person`, `order`, `second`, `0-1 ratio` |
| `displayUnit` | Visible unit, such as `万元`, `人`, `单`, `%`, `分`, `秒` |
| `displayScale` | Scale transform from raw to display, such as `10000 yuan -> 1 万元`, `0.865 -> 86.5%` |
| `precision` | Main UI decimal places or range such as `0`, `1`, `2`, or `0-1 by magnitude` |
| `tooltipPrecision` | More exact decimal places for hover/detail, usually equal or more precise than main UI |
| `exportPrecision` | Export decimal places; must be declared separately for audit/export |
| `roundingMode` | Default `half-up`; use `bankers`, `floor`, `ceil`, or truncation only with business reason |
| `trimTrailingZeros` | Whether `86.0%` can display as `86%`; fixed audit reports usually set `false` |
| `thousandsSeparator` | Default `true` for comparable large values |
| `nullDisplay` | Default `--` for missing/not available values |
| `zeroDisplay` | Default real zero as `0`, `0.0`, or `0%` per contract; never use missing display for true zero |
| `zeroDivisionDisplay` | Default `--`, `不可计算`, or named business copy for denominator `0` |
| `negativeZeroRule` | Display rounded `-0`, `-0.0`, `-0.00%` as `0`, `0.0`, or `0.00%` |
| `smallNonZeroRule` | For tiny rounded-to-zero values, display `<0.1%`, `<0.01`, or tooltip exact value when relevant |
| `formulaPrecisionPolicy` | Recompute rates from numerator/denominator; do not average already rounded rates |

## Default Precision

These defaults apply only when a metric dictionary or project contract does not define stricter rules.

| Value type | Main UI precision | Tooltip/detail precision | Export precision | Notes |
| --- | ---: | ---: | ---: | --- |
| Count, quantity, visits, orders, people | `0` | `0` | `0` | Counts are integers unless the metric is an average |
| Amount with `元` | `0-2` | `2` | `2` | Finance/audit defaults to `2`; management summaries may use `0` |
| Amount scaled to `万元` / `亿元` | `1` | `2` | `2` | Declare scale; avoid mixing `元` and `万元` in one column |
| Currency unit price / average amount | `2` | `2-4` | `2-4` | Keep denominator and weighted-average rule |
| Percent/share/completion/attainment | `1` | `2` | `2` | Raw ratio is usually `0-1`; display as `%` by multiplying `100` |
| YoY/MoM/change rate/variance rate | `1` | `2` | `2` | Color by business direction, not raw sign alone |
| Conversion/funnel rate | `1` | `2` | `2` | Denominator-zero behavior is mandatory |
| Ratio without `%` | `2` | `4` | `4` | Example: input-output ratio `1.35` |
| Score/index `0-100` | `1` | `2` | `2` | If score is integer by governance, use `0` |
| Duration | `0-1` | `1-3` | `3` | Choose unit first: ms, s, min, h |
| Rank/ordinal | `0` | `0` | `0` | No decimal |
| Latitude/longitude | `4-6` | `6` | `6` | Depends on map precision and privacy |
| Scientific/small measurements | By domain | By domain | By domain | Requires explicit domain contract |

## Rounding And Aggregation Rules

- Calculate, aggregate, sort, filter, rank, and reconcile with raw values or source-governed precision, then format for display.
- Percent, share, completion, attainment, conversion, and YoY/MoM must define numerator, denominator, and denominator-zero behavior.
- Totals, subtotals, and grand totals recompute formula metrics from total numerator/denominator. Do not sum displayed percentages or average rounded percentages unless the metric dictionary defines that formula.
- Use one scale per comparable column, axis, legend, KPI group, and export column. If values must use adaptive units, declare the adaptive rule and preserve exact raw value in tooltip/detail.
- When rounded values visually tie, tooltip/detail must expose enough precision to explain ordering or differences.
- Display `-0` as `0`. For tiny non-zero values that round to `0`, use the configured `smallNonZeroRule` if business meaning would be lost.
- Do not encode display values as strings and then reuse them for calculations, sorting, filtering, coloring, thresholds, or export formulas.

## Context Rules

| Context | Rule |
| --- | --- |
| KPI cards | Primary value uses compact precision; tooltip/detail exposes exact value, raw unit, formula, period, source, and denominator when relevant |
| Chart axes | Axis labels may use compact units, but tooltip must show exact value and display unit; axis unit must be visible |
| Chart data labels | Use fewer decimals than tooltip; hide ordinary labels before reducing readability below contract |
| Tables | Numeric cells right-align with tabular numerals; every numeric column declares unit, precision, alignment, null display, and sort basis |
| Pivot/complex tables | Measures carry numeric format contracts; subtotal/grand total formula rules are mandatory for rates |
| Tooltips/drawers | Use `tooltipPrecision` and expose raw numerator/denominator when the number is formula-derived |
| Export | Use `exportPrecision`; include unit/scale in header or metadata; export raw numeric cells when possible, not formatted strings |
| Search/sort/filter | Operate on raw numeric fields, not formatted display text |
| Conditional color/status | Compare raw numeric values against thresholds; display rounding must not flip status |

## Empty, Zero, And Abnormal Values

| Case | Display rule |
| --- | --- |
| Missing/null/not returned | `--` by default; do not display `0` |
| True zero | Display `0` or the metric's fixed zero precision |
| Denominator zero | Display `--` or `不可计算`; tooltip explains denominator |
| Negative value | Allowed only when the metric permits it; color by business meaning |
| Rounded negative zero | Display as zero |
| Tiny non-zero value | Use `< threshold` when business meaning matters |
| Infinite/NaN | Never display raw `NaN`, `Infinity`, or `undefined`; use error/invalid state |
| All-zero composition | Use all-zero state, not fake pie/donut/funnel shares |
| Mixed unit source | Normalize or split before display; do not compare mixed units silently |

## Frontend Implementation Rules

- Use a central number formatter or project utility that consumes `NumericFormatContract` or equivalent metadata.
- Do not scatter `toFixed`, `Math.round`, `parseInt`, string slicing, ad hoc `%` concatenation, or component-local number formatting across Vue/React components.
- View models should carry raw numeric values plus format metadata. Labels are derived at render/export edge only.
- ECharts/S2/Element table formatters must use the same contract for axis labels, data labels, tooltip, table cells, summary rows, and export.
- Component-local filters may change display mode only when the contract declares the metric basis, unit, scale, and precision for each mode.
- Frontend readiness is `partial` or `blocked` if a visible metric has ambiguous `0-1` vs `0-100` percent scale, inconsistent decimals across KPI/chart/table/export, or display rounding drives logic.

## Backend And API Rules

- APIs return structured numeric fields and metadata. Prefer `{ value, unit, scale, precision, rawValue, numerator, denominator }` or a documented equivalent over combined strings such as `"86.5%"`.
- Do not round in SQL/service code before downstream aggregation unless the metric governance contract says the rounded value is the governed business value.
- API docs must declare value type, raw unit, display unit, scale, precision, rounding mode, nullability, denominator-zero behavior, and compatibility impact for every metric field.
- Source/table/upstream replacement must preserve existing response field names, numeric types, units, scale, precision, formulas, and display semantics unless a versioned breaking change is approved.
- Exports generated by backend services must use the same contract as frontend export expectations, with declared export precision and unit headers.

## Readiness Blockers

Do not mark a report artifact, API, frontend implementation, backend implementation, or test handoff `ready` when any of these remain:

- Metric-bearing fields lack `valueType`, raw/display unit, scale, precision, tooltip/export precision, rounding mode, or formatter ownership.
- Percent/rate scale is ambiguous between `0-1`, `0-100`, and already formatted `%`.
- KPI, chart, table, tooltip, drawer, and export show inconsistent decimals or units for the same metric.
- Formula metrics use rounded display values instead of raw numerator/denominator.
- Frontend has scattered ad hoc `toFixed`/`Math.round`/string formatting for governed report metrics.
- Backend returns only formatted strings for data-service metrics that need sorting, filtering, coloring, thresholds, export, or localization.
- Denominator-zero, null, negative zero, tiny non-zero, all-zero composition, or invalid numeric states are undefined.
- Display precision hides a material difference without tooltip/detail exact-value access.
