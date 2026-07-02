# Design Reasonableness Gate

Use this gate after entry consistency has been checked and before irreversible specification, API/model design, frontend/backend implementation, visual repair, or stage handoff.

The goal is to verify that the proposed design is not merely consistent with the inputs, but actually reasonable: it answers the business question, uses the right report logic, has necessary data/API support, keeps filters and interactions meaningful, and can be tested.

## When To Run

Run this gate when any of these are true:

- The task designs, restores, optimizes, repairs, or implements a report/dashboard/prototype/page.
- A workflow converts requirements into component mapping, API lists, data models, API docs, adapters, function descriptions, or test cases.
- A design decision would affect report type, information hierarchy, component choice, metric口径, filter scope, drilldown, action loop, permission behavior, visual layout, or implementation feasibility.
- A requirement document already contains a design idea, page layout, component list, chart choice, or prototype story that downstream work may otherwise implement directly.
- A provided sample/HTML/mock/API can be internally consistent but still not answer the user's real business question.

For narrow copy, typo, or non-design code fixes, record `Design reasonableness: not needed`.

## Audit Dimensions

Check the design across these dimensions:

1. Business fit.
   The design names the user, usage moment, primary question, decision/action, and expected conclusion. The first meaningful viewport answers that question or exposes the correct action entry.
   A good report should reduce one step of thinking for the reader: it declares the primary decision question, the 3-second main point, the conclusion/status before dense evidence, comparison baselines for primary metrics, and the next drilldown/action route. If the user must first infer what question the page is answering, record a `RPT-NO-PRIMARY-QUESTION` or `DESIGN-*` finding.

2. Report-type fit.
   The selected report type matches the task: overview for health/status, diagnosis for why, detail for record lookup, evaluation for scoring/ranking, recap for narrative review, anomaly for alerts, execution for task closure, reconciliation for data correctness.

3. Information hierarchy.
   Content has a clear priority order: conclusion/status, evidence/breakdown, detail, action. It is not a flat wall of equal-weight charts or decorative cards.
   Decision reports follow an inverted-pyramid path: conclusion/judgment -> supporting evidence -> driver/cause -> detail/source -> action/trust. Detail-first layouts are reasonable only for explicit detail-query, reconciliation-first, audit-first, or source-record lookup tasks.

4. Component necessity.
   Every must-have component answers a named business question, has a distinct semantic role, and is not duplicated by another chart with the same message.

5. Metric and data feasibility.
   Metrics have grain, formula, unit, baseline, time scope, dimensions, source or pending gap. Data is sufficient for the chosen chart/table, trend, ranking, funnel, waterfall, Combo, Gauge, parallel coordinates, map, candlestick/K-line, boxplot, heatmap, treemap, sunburst, path chart, Sankey, tree chart, relation graph, or decomposition logic. Analysis & Insight designs specifically need `analysisInsightContract` or equivalent metadata, subtype/family, one conclusion before evidence, evidence or explicit insufficient-data state, affected object/comparison/change/reason/source/freshness when relevant, action/detail/trust/definition disclosure when relevant, local-filter scope, tooltip payload, and loading/empty/error/no-permission/data-delay states. Combo designs specifically need a paired scale + rate/trend/target relationship, shared ordered category/time grain, bar metric/unit, line or target metric/unit, left/right y-axis mapping, dual-axis rationale when present, visible series limit, category-density fallback, legend/filter separation, exact tooltip/detail, and split-chart fallback. Gauge designs specifically need one bounded progress/status metric, min/max range, current value, unit, target/threshold/status semantics, business color direction, clamp/overflow behavior, angle/radius/center geometry, center value hierarchy, and exact tooltip/detail. Funnel designs specifically need ordered stage schema, shared population/cohort logic, metric basis/unit, entry/final values, entry share, stage conversion, drop value/rate, total conversion, stage-count fallback, target/comparison semantics when present, legend/filter separation, and exact stage tooltip/detail. Parallel-coordinate designs specifically need object/sample schema, `3-12` ordered dimensions, per-axis unit/range/direction, independent or standardized scale mode, axis-gap and plot-height budget, sample-density fallback, highlight/brush semantics, and exact object tooltip/detail. Map designs specifically need geography grain, region-code or lon/lat fields, map resource/projection, missing-geo handling, dense point/flow fallback, and exact-value tooltip/detail. Candlestick/K-line designs specifically need ordered OHLC fields, price unit, market color convention, dataZoom/recent-window fallback, missing OHLC/volume states, and exact-value tooltip/detail. Boxplot designs specifically need raw-sample or precomputed-statistics contract, sample counts, Q1/median/Q3/IQR, whisker/outlier rule, category density fallback, and exact five-number tooltip/detail. Heatmap designs specifically need two dimensions plus one numeric metric, aggregation grain, unit, visualMap/color-scale rule, missing-vs-zero encoding, row/column density fallback, and exact cell tooltip/detail. Treemap designs specifically need hierarchy schema, parent/leaf aggregation, non-negative additive area metric, optional color metric semantics, Top N/`其他`, visible-depth rule, label thresholds, breadcrumb/drilldown when deep, and exact path/value/share tooltip/detail. Sunburst designs specifically need hierarchy schema, parent/child aggregation, non-negative additive angle metric, optional color metric semantics, visible depth/ring-width budget, Top N/`其他`, sector label thresholds, center content, breadcrumb/drilldown when deep, and exact path/value/total-share/parent-share tooltip/detail. Path chart designs specifically need step/link schema, start/end/order, metric basis, conversion/drop-off formulas, Top N/aggregation, density fallback, legend/filter separation, and node/link detail evidence. Sankey designs specifically need node schema, source-target-value link schema, layer/stage order, metric unit, non-negative value handling, Top N/`其他`, node/link density fallback, legend/filter separation, and exact node/link share tooltip/detail. Tree chart designs specifically need root node, parent-child schema or children array, depth/layer, visible-depth/default-expanded rule, Top N/`+N` aggregation, density fallback, expand/collapse/search behavior, legend/filter separation, and exact node/parent/child detail evidence. Relation graph designs specifically need node/edge schema, source/target integrity, relationship direction/weight, layout type, density fallback, legend/filter separation, and node/edge detail evidence.
   Composite Panel designs specifically need one shared business topic, a named analysis sequence, `compositePanelContract`, one primary child, child roles/priorities/min sizes, default `2-3` children and normal max `4`, primary visual weight `50-70%`, `contentH >= CH * 0.60`, panel-level local filter scope, child-only filter exception handling, shared legend/unit behavior, linked hover/click context, short detail-preview limit, responsive fallback, and parent/child states. A panel that only groups unrelated widgets for visual richness is a `DESIGN-*` finding.
   Detail Table designs specifically need a row-level lookup/evidence/action task, row grain, primary key/object field, visible column priority, column type/width/alignment, default sort, search/sort/pagination/export execution scope, row detail/action payload, table-body height and visible-row budget, component-local filter limits, and fallback for too many columns or too few rows.
   Complex/grouped table-header designs specifically need real business field groups, `columnTree` or nested grouped columns, leaf field mapping, unit/definition metadata, computed `colSpan`/`rowSpan` or depth/leaf-count rules, max depth `<=3` by default, fixed whole-header behavior, frozen row/primary columns when horizontally scrolling, component-local filter vs per-column header-filter separation, density fallback, tooltip definitions, and enough body-row budget. A grouped header that only adds visual bands without field relationships is a `DESIGN-*` finding.
   Pivot Table designs specifically need a multidimensional cross-summary task, row dimensions, column dimensions, measures, aggregation formulas/functions, subtotal/grand-total semantics, percentage/rate numerator-denominator recomputation rules, hierarchy depth, natural time sorting, S2/project analytical renderer, fixed header/frozen row dimension behavior, density fallback, restrained conditional formatting, exact cell tooltip/drilldown payload, and state handling.
   Primary metrics are unreasonable as isolated display numbers. They should form a relationship network such as result -> driver -> dimension/object -> detail -> action/source. A primary metric without a target, baseline, benchmark, historical range, threshold, denominator, or other explicit comparison basis cannot carry the main judgment.

6. OLAP data modeling fit.
   Reporting/BI/dashboard models name business questions, subject areas, business processes, grain, layer/type, fact/dimension/summary/application role, metric additivity, time口径, conformed dimensions, SCD/history need, many-to-many handling, late-arriving/backfill strategy, quality rules, and lineage. A model that starts from fields or source tables without business process/grain, mixes grains, treats ratios as additive, uses current-only dimensions when historical state matters, or builds an unbounded super-wide table is a `DESIGN-*` finding.

7. Filter and query logic.
   Filters have defaults, option sources, affected components, query params or data fields, permission scope, cascade behavior, and stale-selection behavior.
   Data completeness must be verified before filter binding is accepted: option data, fact/business rows, required fields, default and non-default states, empty/no-permission states, and resolver/API branches must support each affecting primary/global filter.
   A primary/global filter is unreasonable when it only changes selected UI state. Affected components must bind the filter through dataset fields, API/provider/query params, `filterFields`, `requiredFilters`, or resolver params, and non-default filter values must visibly change component data unless the component is explicitly invariant. `ignoredFilters` cannot be used to hide missing mock grain, missing field mapping, or missing resolver logic.
   Business domain, report theme, management object, subject area, and first-level perspective controls are unreasonable as ordinary filters when they change metric names, component set, table headers, metric口径, or domain vocabulary. They must declare `controlSemantics: perspective-switch`, document `componentSchemaImpact`, and live in navigation, route, tab, segment, or explicit perspective state unless proven row-scope-only.
   Navigation percentages, rankings, and status lights are unreasonable without lineage: `sourceDataset`, `field/formula`, `grain`, `affectedFilters`, and `periodBehavior`. Dynamic KPI values must come from business facts, aggregate datasets, or resolvers, not filter option `meta`.

8. Interaction and closure.
   Drilldowns, drawers, jumps, exports, refresh, fullscreen, task actions, approvals, and evidence views preserve the same context and support the user's next step.

9. Visual/layout reasonableness.
   Shell, template, grid, first viewport, block spans, density, labels, legends, tables, and complex diagrams fit the content without duplicate component titles, cramped/narrow/tiny components, overlap, clipping, unreadable text, excessive blank space, or title-node collision. Fixed-height navigation/cards/KPI tiles must declare padding, explicit line-height, gaps, and a passing height budget before acceptance. Page layout owns block placement while each block owns its title/function area; peer component groups use balanced `M * N` layouts when possible; complex diagrams with layer/stage/lane titles must reserve an independent title band and keep titles at least 16px away from the first row of nodes, node borders, child labels, badges, connectors, and edge labels.
   Outer block/grid validity is not enough for composite widgets. Summary zones, nested KPI grids, small metric cells, comparison tiles, and custom card internals must pass fit inside their real sub-containers. Decision-critical metric titles, labels, values, status text, and actions cannot be clipped by `nowrap`/ellipsis without a disclosure path; prefer reserved one- or two-line wrapping, larger min-height, wider zones, stacking, or fewer visible tiles.
   When modern SaaS / BI Dashboard / UI Kit style is requested, reasonableness also requires tokenized light page surfaces, optional analytical surfaces, reduced uniform card borders, stable UI Kit controls, visible first-viewport priority, information flow, no nested-card/component pileup, bounded KPI scope, brand/product color hierarchy before status colors, and lightweight charts. A visually clean but generic, flat, card-heavy, KPI-everywhere, red/green-dependent, or chart-heavy shell is a `VIS-*` or `RPT-*` finding, not a pass.

10. Report data-visualization frontend fit.
   Report/BI/dashboard frontends define user purpose, first-screen conclusion, information hierarchy, chart/table choice, metric names/units/precision/口径, filters, linkage, drill-down/drill-through, tooltip/legend/axis semantics, data freshness/quality display, loading/empty/error/no-permission/stale states, component-ready provider mapping, frontend data-volume/performance limits, theme/color/accessibility, and runtime QA evidence. A design that is a flat chart collection, hides the core conclusion, uses misleading chart types, lacks units/口径, fetches broad data for local global filtering, omits edge states, or cannot trace anomalies to detail is a `DESIGN-*` finding.
   Good-report failures may use stable `RPT-*` IDs from `report-prototype-design-thinking` `references/02-good-report-decision-path.md`, including missing primary question, detail-first hierarchy, flat metric list, missing comparison, missing cause path, missing action path, or static information pileup.

   Existing design ideas inside requirement documents are proposals, not accepted instructions. Before landing them, check whether they preserve the product/report story, user path, information hierarchy, `1920x1080` viewport target, `12 * N` grid, minimum `2*1` block, default `3*2` analytical block, ordinary chart `4*3` maximum, content density, and metric-display boundary. Conflicts are `DESIGN-EXISTING-IDEA-UNVERIFIED` or a more specific `DESIGN-*` finding.

11. API/backend feasibility.
   API endpoints, response models, data models, transformations, auth, pagination, sorting, exports, and error states can support the UI contract without hidden invention. Global/page-level filters and permission scope execute through SQL `WHERE`, source/provider/repository queries, resolver params, Redis/precompute keys, or equivalent source-side scope wherever feasible; component-internal filters may operate on already fetched component data. A design that depends on page/API-level full-materialize-then-filter behavior is a `DESIGN-*` finding unless explicitly bounded.
   Snapshot/latest-period semantics must be modeled as an explicit snapshot role plus shared data-version context (`snapshotDate`, `latestPeriod`, `loadBatch`, `dataVersion`, report version, or source version), not inferred from a project-specific endpoint name. A snapshot/dashboard aggregate API may serve first-screen component data, provide a canonical/shared data cut reused by metrics, trends, rankings, tables, drilldowns, and exports, or both. A design that requires calling one data API first so another API can read an undocumented response or app-memory payload is a `DESIGN-*` finding.
   Data correctness is parameter-driven: version fields, business filters, route/drilldown params, and backend-injected permission/data-scope values must be validated/defaulted before query execution and must map to source predicates, upstream params, precompute lookup keys, or Redis/cache keys. A design that only echoes those values in response metadata after an unscoped/default query is a `DESIGN-*` finding.

12. Report data-service backend fit.
   Report/BI/dashboard backend APIs define a controlled query-service chain: report metadata, dimension/metric/filter/sort whitelist, backend-owned SQL/source expression mapping, parameter guardrails, backend-injected tenant/data/field/export permissions, component-ready result metadata, pagination/count/export strategy, cache key permission safety, data freshness/quality fields, query/export audit, version/publish/rollback, and slow-report governance. A design that lets the frontend send SQL/source expressions, omits permission injection, leaves heavy export synchronous, omits cache permission scope, or cannot explain the report query chain is a `DESIGN-*` finding.
   API design should identify a backend reuse pattern and reusable model family: metadata, filter-options, query, dashboard/snapshot, export, action, or health/status; common request models such as query context/page/export/action; and common response envelopes such as page/options/KPI/series/task/meta. A design that creates one custom controller/query/DTO shape per similar widget without a reason is a `DESIGN-*` finding.
   Data-service responses should separate data from presentation. A design that returns avoidable assembled display copy, business conclusion paragraphs, HTML/Markdown, combined value+unit strings, or style-implied labels instead of structured facts, metadata, reason codes, message keys, and params is a `DESIGN-*` finding unless the text is a documented legal/audit/notification/error/governed-explanation exception.
   Cache, precompute, and snapshot design must keep dependencies explicit: endpoint caches can share invalidation triggers and data-version dimensions, and a declared snapshot can be a shared source of truth, but an undocumented cached response must not become another endpoint's source of truth.
   Redis usage must have a role and operational contract: key template, TTL/invalidation, permission-safety dimensions, miss/stampede behavior, fallback, pool/timeouts, and observability. A design that merely says "use Redis cache" is a `DESIGN-*` finding for production-bound data services.

13. Data-service performance and resilience.
   Production-bound data services have reasonable latency/capacity assumptions, bounded concurrency, cache/precompute design when useful, connection/resource pools, async/offline job strategy for long-running work, timeout/retry/fallback behavior, rate/concurrency limits, health/readiness checks, and observability. A design that relies on unbounded threads/queues, one connection per request, connection acquire without `ApiError`/timeout/exception cleanup, indefinite upstream waits, synchronous handling for long-running work, Redis without timeouts/fallback, or no overload behavior for expensive endpoints is a `DESIGN-*` finding.

14. SQL query reasonableness.
   Database-backed APIs have reasonable query shape: only needed columns are selected, predicates are source-side and sargable, join keys/cardinality are complete, one-to-many multiplication is controlled, dedup/order operations are intentional, pagination is bounded and stable, aggregation/window work happens after early filters when possible, dynamic optional filters avoid broad nullable-OR templates, and risky P0/high-volume queries have plan evidence or a slow-query gap. A design that depends on `SELECT *`, broad in-memory filtering, incomplete joins, deep unbounded pagination, or large unverified sorts is a `DESIGN-*` finding.

15. Report integration testing fit.
   Report/BI/dashboard testing plans define metric口径, golden/baseline data, source/model/API/frontend/export reconciliation, API contract, frontend binding, filters, permissions, cache isolation, export parity, performance/stability, exception states, UAT, release smoke, monitoring, rollback, regression, automation scope, and retest closure when those paths are in scope. A testing plan that only checks page load or API `200`, lacks golden/baseline data for P0 metrics, skips role/tenant/export/cache safety, or cannot localize data mismatches through the chain is a `DESIGN-*` finding.

16. Testability.
   The design has acceptance criteria, validation cases, sample data or runtime evidence, and clear pass/fail behavior for empty, error, no-permission, stale, and edge states.

## Finding Severity

Use stable IDs such as `DESIGN-001`.

- `P0 blocker`: no clear primary question, wrong workflow/report type, key metric/data/API/auth cannot support the design, unsafe permission/action behavior, or the design would lead implementation in a fundamentally wrong direction.
- `P1 high`: important component/filter/interaction/API/model/layout decision is unreasonable or missing and would change user-visible behavior, data correctness, or testability.
- `P2 medium`: design works but has avoidable redundancy, weak hierarchy, incomplete edge states, overly dense layout, or a non-core component with weak justification.
- `P3 low`: wording, small style, ordering, or polish issue that does not affect the design contract.

## Handling Rules

- `P0` findings must be fixed or confirmed before the affected artifact can be marked `ready`.
- `P1` findings must be fixed before implementation unless the user explicitly accepts the limitation and the handoff is marked `partial`.
- `P2` and `P3` findings may be repaired directly when the fix follows existing requirements and does not alter core business/data/API/permission behavior.
- When a design issue is caused by contradictory inputs, also create or link the relevant `ENTRY-*` finding from `entry-input-consistency-gate.md`.
- Do not hide unreasonable design behind "assumption". Assumptions are for unknowns; unreasonable structure needs a `DESIGN-*` finding.

## Output Pattern

```text
Design Reasonableness Audit
Status: pass | partial | blocked | not needed
Findings:
- DESIGN-001 | P1 high | dimension | issue | impact | repair
Decisions:
- DESIGN-001 fixed by ...
Accepted limitations:
- ...
```

## Pass Criteria

- The design has one clear business question and a matching report type.
- The good-report decision path passes or names gaps: 3-second main point, one primary conclusion, comparison basis, cause/location path, drilldown/detail path, and next action.
- Every must-have component, filter, interaction, dataset, and API has a reason.
- Reporting/BI/dashboard data models have explicit business process, grain, layer/type, metric additivity, time口径, quality, and lineage decisions.
- Report data-visualization frontend behavior is feasible when report UI is in scope: first-screen conclusion, appropriate chart/table choices, metric formatting/口径, filters/linkage/drill-through, state coverage, provider mapping, performance limits, and theme/accessibility are explicit.
- Existing requirement-document design ideas are reviewed before implementation and any accepted/repaired/rejected parts are named.
- Affecting filters have field/API/resolver bindings and data-variation evidence for at least one non-default state; selected-state-only filtering is not accepted.
- First-level perspective controls are classified separately from filters, and every schema-changing perspective has component-schema impact plus non-default validation coverage.
- Perspective navigation indicators have lineage, and cross-perspective consistency has at least one concrete field assertion tying navigation data to overview/journey/chart data.
- Fixed-height navigation/cards/KPI tiles have a declared height budget and DOM overflow evidence; `scrollHeight > clientHeight + 2` or `scrollWidth > clientWidth + 2` blocks ready status unless the overflow region is intentional and visibly scrollable or has a declared disclosure strategy.
- Requested modern SaaS / BI Dashboard / UI Kit design has the positive style contract mapped to source hierarchy, tokens, information hierarchy, component count, and chart-lightness checks, with no unresolved `VIS-MODERN-BI-BASELINE-MISSING`, `VIS-GENERIC-SAAS-SHELL`, `VIS-COMPONENT-PILEUP`, `VIS-CHART-OVERWEIGHT`, or `VIS-HIERARCHY-FLAT` finding.
- Analysis & Insight components have `analysisInsightContract`, conclusion-before-evidence, concrete evidence or explicit insufficient-data state, action/trust/source/freshness where relevant, local-filter scope, tooltip/detail disclosure, and stable state geometry.
- Combo charts have a shared ordered x-axis, declared bar/line/target metric roles and units, visible series `<=4`, clear dual-axis rationale when used, category-density fallback, exact tooltip/detail, and a split-chart fallback when the relationship is weak.
- Detail Tables have row grain, primary key/object field, prioritized visible columns, default sort, provider/API/resolver scope for search/sort/pagination/export, row detail/action path, table-body row budget, hidden-field disclosure, and fallback for dense columns or too few visible rows.
- Complex/grouped table headers have business group nodes, real leaf fields, computed span/depth rules, unit/definition disclosure, fixed whole-header behavior, frozen row/primary columns, filter separation, group-to-leaf alignment, density fallback, and a clear reason the table is not better as a flat table, split table, Pivot Table, or drilldown.
- Pivot Tables have row dimensions, column dimensions, measures, aggregation formulas/functions, subtotal/grand-total semantics, rate recomputation rules, S2/project renderer, fixed header/frozen row dimension behavior, `pivotAreaH`/visible-row budget, density fallback, exact cell tooltip/drilldown, and a clear reason they are not a Detail Table or decorative matrix.
- Data completeness was checked before those bindings: filter options, row grain, fields, default/non-default data states, and resolver/API branches are present or documented as blocking gaps.
- Global filter/query behavior is feasible without building or fetching all candidate data before applying scope; component-internal filters are explicitly local to already fetched component data.
- Snapshot/latest-period APIs expose a shared data-version context and explicit snapshot role/reuse rule; metrics/trend/table/export endpoints either reuse the declared snapshot correctly or avoid dependency on undocumented runtime response, frontend call order, or controller memory.
- Data-version, business filters, and permission/data scope constrain backend query params, source predicates, precompute lookups, or cache keys before response construction.
- Composite widget internals fit their sub-containers without hidden critical text, clipped metric titles, or forced fixed grids that make labels unreadable.
- Report data-service backend behavior is feasible when report APIs are in scope: frontend selects codes only, backend owns metadata/query planning/permission injection/guardrails/cache/export/audit/freshness behavior, and no unsafe SQL/source proxy exists.
- Backend reuse is feasible when report APIs are in scope: each production-bound endpoint has a reuse pattern, common request/response model family, and service-layer mapping or an explicit custom-shape reason.
- Redis/cache behavior is explicit when used: role, key dimensions, TTL/invalidation, permission safety, stampede protection, fallback, pool/timeouts, and metrics.
- Database/upstream pool behavior is explicit: pool max such as `STARROCKS_POOL_MAX`, acquire timeout, release/close ownership, `ApiError`/timeout/exception cleanup path, and repeated-failure evidence that the pool is not exhausted.
- Database-backed P0/high-volume APIs avoid obvious SQL query-shape risks or record accepted mitigations/gaps.
- Report integration testing behavior is feasible when report acceptance is in scope: metric口径, golden/baseline data, data-chain reconciliation, API/frontend/filter/permission/cache/export/performance/exception coverage, UAT/smoke/monitoring/rollback, regression, and retest criteria are explicit.
- The first meaningful viewport is useful, not merely attractive.
- Data, filters, interactions, layout, and tests form one traceable contract.
- No unresolved `P0` design issue remains; unresolved `P1` issues are fixed or explicitly accepted as `partial`.
