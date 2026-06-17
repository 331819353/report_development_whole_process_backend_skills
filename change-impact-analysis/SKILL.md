---
name: change-impact-analysis
description: "[后端阶段] 本阶段版本仅服务后端/数据服务设计、API文档/契约、接口实现、运行验证和后端交付；不承接原型设计、前端代码或测试执行。用于需求、指标、口径、筛选、权限、接口、字段、模型、页面或测试变更后的影响分析。用户提到变更影响分析、改指标、改口径、改接口、字段调整、更换数据源/数据表、API返回字段是否保持不变、新增字段规范命名、筛选前数据完整性、需求变更评审、哪些页面/API/模型/前端组件/测试用例/文档受影响、回归范围时触发；不直接修改受影响资产。"
---

# Change Impact Analysis

## Stage Scope

Classification: 后端阶段.

Use this copy only inside the backend/data-service skill bundle. Treat frontend, prototype, and testing work as contracts, evidence, handoff notes, or blockers; do not edit those stages from this skill.

## Overview

Use this skill to turn a change request into a traceable impact package across requirements, pages, components, fields, APIs, data models, metrics, permissions, tests, and delivery documents.

This skill is not a generic change summary. It must identify affected artifacts, owner workflows, regression scope, compatibility risks, and version updates.

## Inputs

- Change request: changed metric, definition, filter, permission, API, source field, page behavior, export rule, SLA, or acceptance rule.
- Current artifacts: requirement brief, prototype, API docs/inventory, data model, metric dictionary, frontend function docs, test matrix, delivery index, defect reports, source code paths, or screenshots.
- Optional: old/new versions, production usage, current release branch, downstream consumers, data owner decision, and deadline.

Read `references/01-impact-matrix-template.md` when producing a reusable matrix.

## Anti-Laziness Gate

For non-trivial work, apply `$quality-gate-validation` `references/anti-laziness-execution-gate.md` before final output, handoff, or readiness. Do not mark the result ready while `LAZY-*` findings remain open, when available local evidence was not inspected, when owning skills were skipped, or when proof is limited to generic statements such as "checked", "optimized", "looks good", or "implemented".

## Workflow

1. Classify the change.
   Identify whether it is metric口径, field/schema, source lineage, source table/upstream replacement, API contract, filter, permission, UI/interaction, export, data quality, SLA, or acceptance change. Mark breaking vs compatible. A source replacement is compatible only when existing API response fields and behavior remain stable and new fields are additive/named by convention.

2. Establish baseline.
   List the current artifact versions and source of truth. If a delivery index exists, use it to anchor which prototype/API/backend/frontend/test/report versions are affected.

3. Trace affected objects.
   Map the changed object to pages, components, fields, APIs, response models, source tables, metric definitions, permission rules, test cases, screenshots, and documents.

4. Assess impact severity.
   Rate each affected item as `breaking`, `behavior-change`, `data-change`, `visual-change`, `test-only`, `doc-only`, or `none`. Include user-facing impact and rollback risk.

5. Define update plan.
   For every affected artifact, state required update, owner workflow, target status, and dependency order. Route to `technical-solution-workflow`, `$api-documentation-design`, `$backend-development-workflow`, `frontend-development-workflow`, `testing-integration-workflow`, `metric-governance-lineage`, or `$delivery-version-management` when that workflow owns the affected artifact.

6. Define regression scope.
   Select API, E2E, screenshot regression, data consistency, filter linkage, permission, export, and data quality cases that must be rerun. For filter changes, put data-completeness regression before filter-binding regression: option data, row grain, required fields, default/non-default states, empty/no-permission states, and resolver/API branches. If automation exists, identify generated test files or case IDs.

7. Produce change decision.
   State whether the change can proceed as patch/minor/major, which blockers must be confirmed, and which downstream artifacts must receive new versions.

## Required Output

- Change summary: old behavior, new behavior, source of request, requested effective version/date.
- Baseline artifact inventory: artifact, version, path/source, owner, status.
- Impact matrix: changed object -> affected page/component/API/model/metric/test/doc, severity, action, owner workflow, status.
- Compatibility and data risk: breaking contracts, historical data/backfill need, cache impact, permission/export impact, rollout/rollback note.
- API response compatibility: preserved fields, additive fields, renamed/removed/reshaped fields, naming compliance, deprecation/versioning, and downstream migration need.
- Regression matrix: case IDs or test categories to run, automation/manual status, evidence needed.
- Filter data-completeness impact before filter-binding impact when filters are changed.
- Version and documentation plan: which artifacts need new versions and delivery index update.
- Blockers/questions: exact decision needed, owner, and affected artifacts.

## Quality Checklist

- Every affected item is traceable to a changed object.
- API/model/frontend/test/doc impacts are not merged into vague wording.
- Breaking changes name downstream consumers and migration strategy.
- Source/table replacement is not a breaking API change by itself; it becomes breaking only when response fields, types, units, precision, enum/null behavior, formulas, grain, or empty/no-permission behavior change without a compatibility layer.
- Regression scope includes data, permission, visual, export, and automation when relevant.
- Filter changes include data-completeness regression before UI/component binding regression.
- No artifact is marked ready while a required source-of-truth decision is unresolved.
