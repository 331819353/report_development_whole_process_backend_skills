# Endpoint Patterns And Splitting

Use this reference to decide API boundaries.

## Common Endpoint Patterns

| Pattern | Use for | Typical trigger |
| --- | --- | --- |
| Metadata | report/page definitions, dimensions, metrics, filters, display metadata | initial-load, publish/refresh |
| Summary KPI | first-screen totals, rates, target attainment | initial-load, filter-change |
| Trend | time-series lines, bars, area charts | initial-load, filter-change |
| Ranking | top/bottom lists, organization/product/customer ranking | initial-load, filter-change, drilldown |
| Structure | distribution, composition, mix analysis | initial-load, filter-change |
| Analytical table | paged detail, metric matrix, S2 table | initial-load, filter-change |
| Detail drawer | row click, chart drilldown, evidence detail | drilldown |
| Filter options | dynamic/cascaded/permission-limited options | initial-load, filter-change |
| Export | file download or async export task | export |
| Action | submit, assign, close, acknowledge, create task | action |
| Health/status | data freshness, source readiness, job/export status | polling, diagnostics |

## Split APIs When

- Default to one data-bearing component or interaction surface per API row. A KPI group, chart, table, drawer, export, dynamic filter option list, and action are separate component/API candidates unless the merge rules below are all satisfied.
- Grains differ, such as monthly KPI vs order-level detail.
- Permissions differ, such as summary visible but detail restricted.
- Refresh cadence differs, such as daily KPI vs real-time alerts.
- Payload sizes differ sharply, such as cards vs paged table.
- Interaction lifecycle differs, such as initial load vs row drawer.
- Export is asynchronous or returns a file/task rather than JSON page data.
- Dynamic filter options need cascades or permission filtering.
- A shared response would force the frontend to split rows, aggregate, rank, compute formulas, filter large arrays, or derive component-specific series/tables from a broad payload.
- The backend would need different query planners, permission services, cache-key families, pagination/export flows, or formatters.

## Merge APIs Only When

- Components load together and form one coherent component group, such as a KPI card group that shares one response model.
- They share the same filters, grain, permission, refresh cadence, and source dependency.
- Payload remains small and coherent.
- The response model remains understandable.
- The backend/API response is already component-ready, so the frontend does not need business aggregation, ranking, formula calculation, or cross-component data reshaping.
- The backend can implement the merged endpoint through one reusable query context, query plan, cache/precompute key family, and formatter.

## Backend Reuse Rules

- Prefer reusable endpoint families over one-off controller shapes: metadata, filter-options, query, dashboard/snapshot, export, action, and health/status.
- A repeated report/list/chart/table pattern should reuse common request models such as query context, pagination, sort, filter, drilldown, and export request.
- A repeated response shape should reuse common envelopes such as page, option item, column metadata, KPI card, series data, task status, and response meta.
- Split or merge decisions should state the backend reuse impact. Reducing HTTP requests is not enough if it creates custom query or formatter logic.
- Fixed bespoke endpoints are acceptable for truly fixed, low-risk reports, but the inventory must state why metadata-driven or common query-service reuse is not needed.

## Snapshot Role And Data-Version Rules

- A snapshot/dashboard aggregate API can be a component-ready view for a particular data cut, a canonical materialized/shared snapshot dataset, or both. Do not assume the name `snapshot` alone decides the role.
- `snapshotDate`, `latestPeriod`, `loadBatch`, `dataVersion`, source version, permission scope, and report version may be shared across endpoints as request params, response metadata, or cache-key dimensions.
- Metrics, trends, rankings, tables, drilldowns, and exports must build their own response from source/logical models, repository queries, precompute tables, or Redis/cache entries filtered by that shared data-version context and the correct business/permission scope.
- Metrics, trends, rankings, tables, drilldowns, and exports may instead reuse a declared canonical snapshot response or materialized snapshot when the API inventory records matching grain, filters, permission scope, data-version params, fields, cache key, and invalidation behavior.
- For each data-bearing endpoint, inventory the query params that constrain data: version/date params, business filters, route/drilldown params, pagination/sort params, and backend-injected tenant/user/role/data-scope params. These params must map to source predicates, precompute lookup keys, or cache-key dimensions.
- Do not merge or split APIs in a way that requires undocumented frontend call order such as "call snapshot first, then metrics reads whatever payload happens to be in memory".

## Forbidden Shortcuts

- Do not make one API for an entire complex report unless the page is truly static and small.
- Do not create separate APIs for every tiny visual mark when one coherent model supports them.
- Do not create a new controller/query/DTO shape for every similar KPI, chart, table, or export when a shared query-service pattern can serve them.
- Do not merge several independent components into one API merely to reduce request count when doing so moves business calculation, filtering, grouping, ranking, or response splitting into the frontend.
- Do not treat one data-bearing API response as the hidden in-memory data source for another endpoint. Declared snapshot reuse is acceptable; undocumented app-memory reuse is not.
- Do not treat version and scope fields as response decoration only. If they affect correctness, they must constrain the backend query or cache lookup.
- Do not hide dynamic filter option data inside unrelated business data.
- Do not treat export as a frontend-only action when server-side permission, volume, or async generation is needed.
