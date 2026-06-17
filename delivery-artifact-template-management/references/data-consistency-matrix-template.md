# Data Consistency Matrix Template

Use this template when comparing backend API responses with frontend display values.

## Component Comparison Columns

| Component | API endpoint | Request params | controlSemantics | componentSchemaImpact | Navigation metric lineage | Cross-perspective consistency proof | Data completeness before filter binding | Response fields | Adapter/formula | Display fields | Expected value | Actual value | Evidence | Env/version/data context | Retest defect ID | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Required Checks

- KPI cards, charts, tables, drawers, exports, and drilldowns.
- Units, precision, date/period format, sorting, Top N, totals/subtotals, null/empty values.
- Backend response -> adapter output -> rendered UI value trace.
- Control semantics and schema impact for perspective switches, global filters, local filters, and drilldown params.
- Navigation metric lineage for percentages, rankings, and status lights: `sourceDataset`, `field/formula`, `grain`, `affectedFilters`, `periodBehavior`.
- Active filters and permissions used by the request.
- Non-default perspective checks: metric names, titles/summaries, table dimensions/headers, component set, specialty metrics, risk focus, and口径 labels.
- Cross-perspective consistency checks: navigation percentages, overview KPIs, journey cards, and chart summaries use the same data chain; at least one field-level assertion is recorded.
- Before judging filter binding, prove data completeness: option data, default response, at least one non-default response or row set, required fields, and resolver/API branch coverage. A single default snapshot is a data gap for affecting filters.
- Production/retest context when applicable: environment, version/build, account/role, data seed/source mode, defect ID, and closure criteria.

## Mismatch Classification

- Backend contract mismatch.
- Frontend adapter/binding mismatch.
- Data completeness/data grain mismatch.
- Control semantics or perspective-schema mismatch.
- Navigation metric lineage or cross-perspective consistency mismatch.
- Filter/request parameter mismatch.
- Mock/static data residue.
- Display formatting or precision mismatch.
