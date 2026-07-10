---
name: report-delivery-pipeline-governance
description: "[后端阶段] 本阶段版本仅服务后端/数据服务设计、API文档/契约、接口实现、运行验证和后端交付；不承接原型设计、前端代码或测试执行。用于治理报表项目从需求、原型、数据模型、API、后端、前端、测试到发布/复测的交付链路、阶段交接和ready/partial/blocked判定。用户提到交付链路、阶段门禁、上下游交接、需求到原型/API/前后端/测试是否闭合、artifact contract、handoff、哪个阶段该走哪个skill、跨阶段缺口时触发；不替代单个阶段的具体实现。"
---

# Report Delivery Pipeline Governance

## Stage Scope

Classification: 后端阶段.

Use this copy only inside the backend/data-service skill bundle. Treat frontend, prototype, and testing work as contracts, evidence, handoff notes, or blockers; do not edit those stages from this skill.

## Positioning

Use this skill to keep report delivery stages aligned and to decide whether a handoff can proceed across requirement, prototype, data model, API, backend, frontend, testing, release, defect repair, and production feedback.

Use `$delivery-version-management` for version indexes and release bundles. Use `$quality-gate-validation` for concrete gate findings when checking a specific artifact or implementation. For prototype-derived backend work, apply `backend-development-workflow/references/00-prototype-downstream-handoff-contract.md` and treat its fixed PRD/child-backend baseline, prototype/source version, data summary, stable-ID/API/source trace, mock replacement, table understanding, request predicate, and runtime evidence as the handoff contract.

For standalone backend development, apply `backend-development-workflow/references/01-standalone-new-project-contract.md`. The user requirement, writable root, stack decision, service/API/source/predicate matrices, implementation evidence, auth/env, tests/build/runtime, and gaps form the delivery chain; prototype artifacts are not required.

## Reference Loading

- Read `references/report-delivery-pipeline-contract.md` before judging cross-stage handoff completeness, stage routing, or delivery-chain readiness.
- Use `$artifact-readability-standard` when the handoff artifact needs dual-readable structure.
- Use `$environment-profile-contract` for runtime profile readiness.
- Use `$code-change-ledger-management` when source code changed.

## Anti-Laziness Gate

For non-trivial work, apply `$quality-gate-validation` `references/anti-laziness-execution-gate.md` before final output, handoff, or readiness. Do not mark the result ready while `LAZY-*` findings remain open, when available local evidence was not inspected, when owning skills were skipped, or when proof is limited to generic statements such as "checked", "optimized", "looks good", or "implemented".

## Workflow

1. Identify current stage, upstream artifacts, downstream consumers, and claimed readiness.
2. Map the stage to required handoff artifacts and owning skills.
2A. Classify backend work as standalone, existing-project, or prototype-derived before requiring upstream artifacts.
3. For PRD/prototype-derived work, inventory targeted reading rows, consumed PRD execution files, `docs/prototype-data-summary.md`, component data keys, replacement rows, metric/source/interface rows, filters, actions, exports, details, conclusion inputs, and open `ENTRY-*` / `GAP-*`.
3A. For backend, verify `prototypeBaselineRecord`, `prototypeContractConsumptionMatrix`, `prototypeConfigurationTraceMatrix`, `mockToRealBackendMatrix`, `tableContentUnderstandingMatrix`, `requestParamPredicateMatrix`, and API/source/code/test/runtime evidence.
4. Check that stable IDs, versions, sources, gaps, evidence, code ledgers, environment profiles, and readiness values link across stages.
5. When backend/API implementation is in the path, check minimal interface evidence: table-content understanding, filters as request params mapped to source predicates, source-query-simple query-only boundary, and derived/summary exceptions or gaps.
6. Route missing or conflicting work to the owning skill instead of absorbing implementation details.
7. Return a stage verdict and next-stage entry criteria.

## Required Output

- Current stage and target next stage.
- Required upstream/downstream artifacts and missing pieces.
- Targeted reading / PRD / data-summary consumption matrix when applicable.
- Minimal interface implementation evidence when backend/API work is in scope.
- Owning skill routing for each gap or blocker.
- Readiness: `ready`, `partial`, or `blocked`.
- Next-stage handoff requirements.

## Quality Gate

- Do not mark a stage ready when required upstream contracts, evidence, versions, profile decisions, code ledgers, or test results are missing.
- Do not mark a downstream stage ready for PRD/prototype-derived work when targeted reading rows, the PRD execution bundle, `docs/prototype-data-summary.md`, replacement rows, component data keys, metric/source/interface mappings, filter/action/export/detail/conclusion ownership, or downstream version evidence is missing or stale.
- For `backendEntryMode = prototype-derived`, do not mark backend handoff ready when any requirement in `backend-development-workflow/references/00-prototype-downstream-handoff-contract.md` is missing or stale. For standalone work, use `01-standalone-new-project-contract.md` and never treat prototype absence as a blocker.
- Do not mark backend/API handoff ready when table-backed interfaces lack table-content evidence, client-visible filters are not request params mapped to source predicates, or simple retrieval endpoints hide joins, aggregation, exact counts, formulas, totals, rankings, or broad processing.
- Do not let a later-stage implementation silently redefine requirement, metric, API, source, permission, or test contracts.
