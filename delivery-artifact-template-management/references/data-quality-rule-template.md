# Data Quality Rule Template

| Rule ID | Object/table/API | Field/metric | Quality dimension | Rule expression | Threshold | Frequency | Owner | Evidence query/API | Failure action | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DQ-001 |  |  | completeness / uniqueness / timeliness / accuracy / validity / outlier / drift / consistency |  |  |  |  |  |  | not run |

## Quality Dimensions

- `completeness`: required fields, partitions, periods, or rows exist.
- `uniqueness`: primary/business keys are unique at the expected grain.
- `timeliness`: data refresh completes within SLA and uses the expected business date.
- `accuracy`: values match source-of-truth, formula, reconciliation, or approved baseline.
- `validity`: enum, range, format, unit, precision, and date rules are valid.
- `outlier`: abnormal spikes/drops or impossible values are flagged.
- `drift`: metric definition, source, or distribution shifts unexpectedly.
- `consistency`: totals match across source systems, APIs, reports, exports, and frontend displays.
