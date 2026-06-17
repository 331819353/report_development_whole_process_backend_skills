# Model File Template

Use this exact structure when producing a 数据模型文件.

## 1. Model Overview

| Field | Value |
| --- | --- |
| Document purpose | TBD(GAP-*) |
| Document version | TBD(GAP-*) |
| Updated at | TBD(GAP-*) |
| Supported pages/modules | TBD(GAP-*) |
| Related API IDs | TBD(GAP-*) |
| Data owner | TBD(GAP-*) |
| Model owner | TBD(GAP-*) |
| Decision source | TBD(GAP-*) |
| Status | partial |
| Gap IDs | TBD(GAP-*) |

## 2. Business Analysis Matrix

| Consumer/role | Business question | Subject area | Business process/object | Required metrics | Required dimensions | Required filters | Traceability need | Status | Gap IDs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## 3. Data Sources

| Source ID | Source name | Type | Location | Owner | Refresh cadence | Permission rule | Reliability notes | Status | Gap IDs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Allowed source types: `table`, `view`, `file`, `upstream-api`, `manual`, `derived`, `unknown`.

## 4. Source Models

| Source model ID | Source ID | Layer | Model type | Physical object | Subject area | Business process/object | Business meaning | Grain | Primary key | Natural keys | Business time field | Date/partition field | Update mode | Field count | Status | Gap IDs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Layer values: `ODS`, `DWD`, `DIM`, `DWS`, `ADS`, `external`, `unknown`.

Model type values: `transaction-fact`, `periodic-snapshot-fact`, `accumulating-snapshot-fact`, `factless-fact`, `dimension`, `bridge`, `summary`, `wide`, `application`, `source`, `unknown`.

Update mode values: `full`, `incremental`, `zipper/scd`, `snapshot`, `event`, `manual`, `unknown`.

Field metadata:

| Source model ID | Physical field | Business label | Type | Dimension/measure | Additivity | Unit | Enum/range | Nullable/default rule | Sensitivity | Sample value | Quality note | Gap IDs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Additivity values: `additive`, `semi-additive`, `non-additive`, `none`, `unknown`.

## 5. Logical Models

| Logical model ID | Subject area | Business process/object | Layer | Model type | Source models | Grain | Keys | Business time field | Relationships | History/SCD rule | Summary/wide-table need | Owner | Status | Gap IDs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Relationship metadata:

| From model | To model | Join keys | Cardinality | Join type | Required? | Many-to-many/bridge rule | Allocation/dedup rule | Quality risk | Gap IDs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## 6. Response/View Models

| Response model ID | Used by APIs/pages | Row grain | Backing logical model | Layer/source layer | Sort/default order | Empty-state behavior | Frontend/API serving note | Status | Gap IDs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Field metadata:

| Response model ID | Response field | Display label | Type | Source/logical mapping | Calculation | Unit | Precision | Enum labels | Null rule | Sensitivity | Masking/field permission | Example | Gap IDs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## 7. Metrics

| Metric ID | Metric name | Metric type | Formula | Numerator | Denominator | Additivity | Grain | Dimensions | Time口径/business time field | Period logic | Dedup rule | Unit | Precision | Direction | Baseline/threshold | Source dependency | Reconciliation rule | Gap IDs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Metric type values: `atomic`, `derived`, `composite`.

## 8. Transformation Mapping

| Mapping ID | Source field/model | Logical field/model | Response field/model | Transformation | Grain change | Time口径 | Permission filter | Quality check | Gap IDs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## 9. Security Rules

| Rule ID | Target model/field | Sensitivity | Masking rule | Field-level permission | No-permission behavior | Gap IDs |
| --- | --- | --- | --- | --- | --- | --- |

Sensitivity values: `public`, `internal`, `confidential`, `sensitive`, `unknown`.

## 10. Data Quality Rules

| Rule ID | Target model/field | Rule type | Rule description | Severity | Handling | Gap IDs |
| --- | --- | --- | --- | --- | --- | --- |

Rule types: `uniqueness`, `completeness`, `enum-validation`, `range-check`, `freshness`, `referential-integrity`, `reconciliation`, `dimension-hit-rate`, `metric-fluctuation`, `deduplication`, `backfill-readiness`.

## 11. Layering, Summary, And Wide-Table Decisions

| Decision ID | Target model/API/page | Decision type | Query pattern or business reason | Selected layer/model | Grain | Dimensions retained | Metrics retained | Redundancy rule | Traceability path | Status | Gap IDs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Decision type values: `layering`, `summary`, `wide-table`, `ads-application`, `multi-period`, `history-snapshot`, `bridge`, `none`.

## Blank Cell Rule

Do not leave required cells blank. Use `none` when intentionally not applicable, or `TBD(GAP-*)` when unknown. A row with `TBD(GAP-*)` cannot be `ready`.
