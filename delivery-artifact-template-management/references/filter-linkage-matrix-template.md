# Filter Linkage Matrix Template

Use this template to prove every control is classified first, then every filter has data completeness before request mapping, affected components, and edge-state behavior.

## Filter Matrix Columns

| Control/filter | controlSemantics | componentSchemaImpact | Navigation metric lineage | Option source | Data completeness before binding | Default/non-default data proof | Cross-perspective consistency proof | Request field/param | Binding method | Affected components | Reset behavior | Edge cases | Env/version/role context | Retest defect ID | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Interaction Matrix Columns

| Action | Source component | Active filters inherited | Target request/action | Expected state update | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |

## Required Edge Cases

- Data completeness before binding: option rows, matching fact/business rows or API/provider responses, required fields, default state, at least one non-default state, empty/no-permission state when relevant, and resolver/API branches for scenario filters.
- Control semantics: perspective switches, global filters, local filters, and drilldown params are separated before filter linkage judgment.
- Non-default perspective: metric names, titles/summaries, table dimensions/headers, component set, specialty metrics, risk focus, and口径 labels update when `componentSchemaImpact` requires them.
- Navigation metric lineage: percentages, rankings, and status lights declare `sourceDataset`, `field/formula`, `grain`, `affectedFilters`, and `periodBehavior`.
- Cross-perspective consistency: navigation percentages, overview KPIs, journey cards, and chart summaries reconcile to the same data chain for each domain/statistical口径; include at least one field assertion such as navigation satisfaction equals current `experienceProfiles.satisfaction`.
- Empty option list.
- Invalid/expired option.
- All option or cleared selection.
- Multi-select encoding.
- Cascade parent change clears invalid child values.
- Permission-limited options.
- Export, drawer, pagination, sorting, jump, and refresh inherit active filters when required.
- Production/retest context when applicable: environment, version/build, account/role, data seed/source mode, defect ID, and closure criteria.

## Pass Rule

Do not mark filter linkage `pass` when data completeness is missing or only one default snapshot exists for an affecting filter. Record that as a data-completeness/data-grain gap before judging UI or component binding. Do not mark a schema-changing perspective `pass` when it is modeled only as a normal filter, only changes values while labels/schema stay default, lacks navigation metric lineage, or fails cross-perspective consistency.
