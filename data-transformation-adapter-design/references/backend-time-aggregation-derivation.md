# Time Aggregation Derivation

Use this reference for time normalization, aggregation, formulas, sorting, ranking, and reconciliation.

## Time And Period Rules

- Define input format, output format, timezone, locale, and calendar/fiscal calendar.
- Specify whether `YYYYMMDD -> YYYYMM` is truncation, calendar aggregation, fiscal-period mapping, or another business rule.
- Define date-range inclusivity and boundary behavior.
- Define invalid, missing, future, or out-of-range date handling.
- Keep displayed periods stable across API docs, code, tests, and frontend adapters.

## Aggregation Rules

- Define group keys and output grain.
- Define aggregation method for each measure: sum, count, distinct count, min, max, average, weighted average, last value, first value, median, percentile, or custom formula.
- Define denominator rules for rates and ratios.
- Define total/subtotal behavior and whether totals reconcile with visible rows or full filtered rows.
- Define sorting, Top/Bottom, tie-breakers, and stable ordering.
- Define sparse data behavior, missing buckets, zero-fill, null-fill, and no-data response shape.

## Business Derivations

Document formulas for:

- Completion, gap, rate, ratio, contribution, YoY, MoM, CAGR, score, rating, risk level, overdue days, aging bucket, DSO, DIO, SLA status, and other derived fields.
- Precision, rounding mode, percentage scaling, unit conversion, and display unit.
- Error behavior for divide-by-zero, missing denominator, negative values, and inconsistent source rows.

## Reconciliation

- Include at least one sample that reconciles source rows to output totals or derived fields.
- Explain allowed differences caused by rounding, permission scope, late-arriving data, filters, cache windows, or upstream lag.
- Flag unreconciled totals as contract failures or missing information.
