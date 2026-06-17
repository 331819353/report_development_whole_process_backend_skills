---
name: quality-gate-validation
description: "[后端阶段] 本阶段版本仅服务后端/数据服务设计、API文档/契约、接口实现、运行验证和后端交付；不承接原型设计、前端代码或测试执行。用于执行跨阶段质量门禁和一致性检查。用户提到质量检查、开工前理解门禁、行动前自省、反懒性执行门禁、证据不足不能ready、过程中反思做得对不对、输入材料冲突、入口一致性、设计合理性、筛选绑定断裂、快照接口依赖、snapshotDate/dataVersion/loadBatch、指标单位/百分比显示冲突、更换数据源/数据表后API字段漂移、新增字段命名不规范、生产就绪、验收门禁、可交付性、不要凭空假设、需求/API/模型/前端/后端/测试不一致、ready/partial/blocked 判定时触发；不替代具体实现 skill。"
---

# Quality Gate Validation

## Stage Scope

Classification: 后端阶段.

Use this copy only inside the backend/data-service skill bundle. Treat frontend, prototype, and testing work as contracts, evidence, handoff notes, or blockers; do not edit those stages from this skill.

## Positioning

Use this skill to decide whether an artifact, implementation, handoff, or workflow stage is `ready`, `partial`, or `blocked`. It detects cross-stage conflicts, missing evidence, unsafe assumptions, visual/runtime issues, production readiness gaps, and delivery-chain breaks.

It is a gate, not a dumping ground for domain implementation. Load the owning skill references for domain details, then use this skill to judge readiness and route unresolved findings.

## Reference Loading

Primary shared gates:

- `references/preflight-understanding-gate.md`
- `references/anti-laziness-execution-gate.md`
- `references/entry-input-consistency-gate.md`
- `references/design-reasonableness-gate.md`
- `references/production-closed-loop-readiness.md`
- `references/visual-multimodal-browser-check.md`, then `visual-browser-regression-check` for screenshot, baseline diff, multimodal visual review, and `VIS-*` findings.
- `references/human-ai-readable-artifact-standard.md`, then `$artifact-readability-standard` for human-readable and AI-extractable artifact structure.
- `references/report-delivery-pipeline-contract.md`, then `$report-delivery-pipeline-governance` for cross-stage handoff and delivery-chain contracts.
- `references/environment-profile-contract.md`, then `$environment-profile-contract` for test/production profile separation and runtime config handoff.
- `references/shared-quality-gate-blockers.md`
- `$code-change-ledger-management` when frontend/backend/prototype code changed.
- `haier-enterprise-app-ui-design-spec` when judging Haier/enterprise Web UI readiness, including report/dashboard pages that inherit company-level application UI rules.
- `$metric-number-display-contract` when judging numeric unit, precision, rounding, percent, tooltip/export, or formatter ownership.
- `report-design-system-governance` relevant references when judging report/dashboard/BI/data-screen readiness.
- report-design-system-governance reference 12-modern-saas-bi-style-contract.md when modern SaaS / BI Dashboard / UI Kit style is requested or claimed.

## Gate Types

| Gate | Use when |
| --- | --- |
| Preflight understanding and action reflection | Before implementation, repair, QA, acceptance, or any workflow with multiple possible owning skills or artifact authorities; repeat before non-trivial actions while work is underway. |
| Anti-laziness execution | Non-trivial work needs evidence-first execution, owning-skill proof, before/after proof, regression probe, and `No proof, no ready` enforcement. |
| Entry consistency | Inputs disagree on requirement, metric, source, API, field, permission, UI, env, runtime, or test evidence. |
| Design reasonableness | A design is internally consistent but may not serve the business question, data shape, workflow, permission model, or testability. |
| Production readiness | A handoff claims real delivery or release readiness. |
| Visual/runtime gate | Runnable UI needs screenshot, baseline diff, multimodal review, or visual defect triage. |
| Artifact readability | Outputs must be human-readable and downstream-agent-readable. |
| Environment profile | Runtime profiles, URLs, proxy/CORS, auth, deployment, and rollback must be separated. |
| Delivery pipeline | Handoffs must stay aligned across requirement, prototype, model, API, backend, frontend, test, release, and retest artifacts. |
| Code change ledger | Changed code needs file-level traceability, pre-change read evidence, code ranges, verification, and rollback/blocker notes. |
| Backend logging | Backend/data-service readiness depends on diagnosable structured logs. |
| Numeric precision/display | Metric-bearing artifacts need consistent value type, units, scale, precision, rounding, null/zero behavior, and formatter ownership. |
| Haier/app UI baseline | Haier/enterprise Web pages, including report/dashboard pages, need company UI baseline checks for tokens, base controls, states, brand/logo, and responsive behavior. |
| Report UI baseline | Report/dashboard/analysis pages need report guideline checks. |
| Modern BI style baseline | Requested modern SaaS / BI Dashboard / UI Kit pages need tokenized light surfaces, white-card UI Kit language, hierarchy, no component pileup, and lightweight chart proof. |

## Workflow

1. Run the Preflight understanding gate when the next step could edit, repair, test, accept, or route non-trivial work.
2. During execution, repeat the action reflection loop from `preflight-understanding-gate.md` before non-trivial design/code/QA actions, especially when new evidence changes the source authority, renderer, data contract, or visual source.
3. Run the Anti-laziness execution gate for implementation, repair, QA, acceptance, or handoff work that could otherwise pass with thin evidence.
4. Select the smallest additional gate set needed for the current risk.
5. Classify affected artifacts and owning skills.
6. Load the relevant shared gate references and domain baseline references.
7. Inventory evidence and conflicts.
8. Produce findings with stable IDs such as `PREFLIGHT-*`, `LAZY-*`, `ENTRY-*`, `DESIGN-*`, `READY-*`, `VIS-*`, `VDIFF-*`, or domain-specific IDs.
9. Assign severity, owner, affected artifact, required evidence/action, and readiness impact.
10. Mark each affected artifact `ready`, `partial`, or `blocked`.
11. Route unresolved findings to the owning skill/workflow.

## Required Output

- Gate(s) executed and evidence checked.
- Action reflection decisions when the gate covers implementation, repair, renderer choice, HTML/sample conversion, or readiness judgment.
- Anti-laziness findings or explicit no-finding result when the work is implementation, repair, QA, acceptance, or handoff.
- Proof obligations and pass/fail evidence when visual/layout/component contracts are part of the readiness claim.
- Rule strength audit when a standard/spec contains advisory wording that may affect correctness, runtime fit, renderer ownership, data trust, filters, permissions, accessibility, or readiness.
- Findings table with ID, severity, expected, actual, impact, owner, required action, and readiness impact.
- Readiness result: `ready`, `partial`, or `blocked`.
- Confirmation questions only for decisions that block affected work.

## Quality Gate

- Do not mark `ready` when high-impact conflicts, missing production controls, missing runtime evidence, or untested required behavior remain.
- Do not mark non-trivial implementation, repair, QA, or acceptance work `ready` when the affected surfaces, owning skills, hard constraints, and start decision from `preflight-understanding-gate.md` are missing.
- Do not mark non-trivial implementation, repair, QA, or acceptance work `ready` when the work passed initial preflight but skipped action reflection before later design/code/QA decisions that changed constraints, renderer, source authority, or visual source.
- Do not mark non-trivial work `ready` while blocking `LAZY-*` findings remain, or when the only evidence is a generic statement such as "checked", "optimized", "looks good", or "implemented".
- Do not mark visual/layout/component contract work `ready` when contracts exist only in prose/config and lack matching DOM/CSS/renderer/browser evidence. Use `LAZY-CONTRACT-THEATER` or a domain `VIS-*`/`RPT-*` finding.
- Do not let advisory wording hide a required constraint. If a `should`/`recommended`/`prefer`/`default` rule affects correctness, runtime fit, renderer ownership, data trust, filter/query/export/permission behavior, accessibility, or readiness evidence, it must be treated as `MUST/fail` or documented as `SHOULD/exception-required` with evidence.
- Do not mark Haier/enterprise report or dashboard UI `ready` when report-specific checks pass but inherited Haier application UI baseline checks are missing or treated as optional.
- Do not mark a requested modern SaaS / BI Dashboard / UI Kit page `ready` when the positive style contract is missing, the layout is a generic SaaS shell, components are piled up, charts are overweight, or hierarchy is flat.
- Do not mark `ready` when governed report metrics lack numeric display contracts or show inconsistent units, decimals, percent scale, rounding, tooltip/export precision, null/zero/denominator-zero behavior, or formatter ownership across design/API/frontend/backend/export.
- Do not use this skill to restate full domain rules; cite the loaded references and summarize the blocking evidence.
- Load `shared-quality-gate-blockers.md` before final readiness decisions or when a finding can block delivery.
