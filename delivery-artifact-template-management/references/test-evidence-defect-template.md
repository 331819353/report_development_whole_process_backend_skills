# Evidence And Defect Template

Use this template when producing a handoff-ready test report.

## Evidence Item

- Case ID:
- Environment:
- URL/API:
- Preconditions:
- Steps:
- Expected result:
- Actual result:
- Evidence: screenshot path, network sample, console log, API response, or source path.
- Headless screenshot: path, viewport, page/state, capture time.
- Deterministic visual diff: `VDIFF-*` ID, baseline path, current path, diff path, threshold, result.
- Multimodal visual finding: `VIS-*` ID, category, severity, component/region, observation, impact.
- Status: pass / fail / blocked.

## Defect Item

- Defect ID:
- Severity: blocker / major / minor.
- Owner side: frontend / backend / contract / data / environment / unknown.
- Reproduction steps:
- Expected result:
- Actual result:
- Data completeness checked before filter binding: yes / no / not applicable.
- Data completeness evidence: option rows, default rows, non-default rows, required fields, resolver/API branch, empty/no-permission state.
- Filter binding evidence: request params, provider params, `filterFields`, `requiredFilters`, `ignoredFilters`, visible value/row-set/series/total change.
- Control semantics evidence: `perspective-switch`, `global-filter`, `local-filter`, or `drilldown-param`.
- Component schema impact evidence: metric names, titles/summaries, table dimensions/headers, component set, specialty metrics, risk focus, and口径 labels for non-default perspectives.
- Navigation metric lineage evidence: `sourceDataset`, `field/formula`, `grain`, `affectedFilters`, `periodBehavior`.
- Cross-perspective consistency evidence: navigation percentages, overview KPIs, journey cards, chart summaries, and at least one field-level equality assertion.
- Fixed-height budget/DOM evidence: component height, padding, explicit line-height rows, gaps, badge/status/footer heights, `requiredContentHeight <= componentHeight`, viewport, `scrollHeight/clientHeight`, and `scrollWidth/clientWidth`.
- Donut/pie crop and budget evidence: crop path, `legendBandHeight`, `labelLineBudget`, `radius`, `center`, right-legend width budget if used, low-value label handling, tooltip/legend disclosure, and title/legend/label-line/label/center boundary result.
- Connection-pool leak evidence: pool type/source, max config such as `STARROCKS_POOL_MAX`, repeated `ApiError`/timeout/exception reproduction count, acquire/release logs or active/idle counts, later-request acquire result, and cleanup path (`finally`/context manager/equivalent).
- Evidence:
- Screenshot:
- Baseline/current/diff artifact:
- Visual finding:
- Likely cause:
- Filter defect classification order: data completeness/data grain -> API/provider contract -> frontend/filter binding.
- Missing information:
- Status: open / fixed / retest / closed / blocked / accepted.
- Suggested fix:
- Retest criteria:
- Retest evidence:

## Final Conclusion

State `pass`, `partial pass`, `fail`, or `blocked`, list unresolved blockers separately from ordinary defects, and include open/fixed/retest/closed/blocked defect counts when the report is used for production acceptance.
