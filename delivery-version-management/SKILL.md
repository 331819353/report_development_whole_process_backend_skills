---
name: delivery-version-management
description: "[后端阶段] 本阶段版本仅服务后端/数据服务设计、API文档/契约、接口实现、运行验证和后端交付；不承接原型设计、前端代码或测试执行。用于报表项目交付物版本管理、交付物索引、版本链路和迭代追踪。用户提到版本化交付、原型/API/数据模型/后端/前端/测试报告版本对应关系、交付物索引、版本对齐、迭代记录、发布包清单、哪个文档对应哪个版本时触发；不负责生成各交付物正文。"
---

# Delivery Version Management

## Stage Scope

Classification: 后端阶段.

Use this copy only inside the backend/data-service skill bundle. Treat frontend, prototype, and testing work as contracts, evidence, handoff notes, or blockers; do not edit those stages from this skill.

## Overview

Use this skill to create a single delivery index that links prototype, requirements, API docs, data models, backend, frontend, test reports, automation, defects, and release notes across iterations. Use `$code-change-ledger-management` for reusable file-level code change ledger discipline on frontend, backend, and runnable prototype source code.

The goal is to answer: "Which version of each artifact belongs together, and what changed?"

## Inputs

- Artifact folders/files, current version naming, PRD/prototype/API/model/frontend/backend/test documents, release notes, branch/commit, environment, or defect reports.
- Prototype-derived delivery inputs: PRD execution bundle, `docs/prototype-data-summary.md`, Mock API To HTTP API Replacement Matrix, Metric To Interface / Source Mapping, component data-key list, and open `GAP-*`.
- Optional: target version, release date, owner, status, dependency chain, and change request IDs.
- Frontend/backend/prototype source code paths when the delivery index must link to per-file ledgers, changed code ranges, or implementation traceability.

Use `$delivery-artifact-template-management` when producing the delivery index table. Use `scripts/build_delivery_index.py` to create a first-pass index from files.
Use `$code-change-ledger-management` when source code is created, edited, repaired, or refactored.

## Reference Loading

- Code-file ledger structure and sidecar expectations: `references/code-file-change-ledger.md` when the delivery index must link changed frontend/backend/prototype source files to file-level ledgers.

## Anti-Laziness Gate

For non-trivial work, apply `$quality-gate-validation` `references/anti-laziness-execution-gate.md` before final output, handoff, or readiness. Do not mark the result ready while `LAZY-*` findings remain open, when available local evidence was not inspected, when owning skills were skipped, or when proof is limited to generic statements such as "checked", "optimized", "looks good", or "implemented".

## Workflow

1. Define version chain.
   Use a stable chain such as `requirement-v1 -> prototype-v1 -> model-v1 -> api-v1 -> backend-v1 -> frontend-v1 -> test-v1 -> release-v1`. Keep patch/minor versions when one artifact updates without full-cycle redesign.

2. Inventory artifacts.
   List every artifact path, type, version, owner, source date, status, and related change IDs. Mark missing or stale artifacts.
   For prototype-derived report work, inventory the PRD execution files, `docs/prototype-data-summary.md`, replacement rows, metric/source/interface rows, component data keys, and `GAP-*` items as versioned artifacts.

3. Link dependencies.
   Connect each artifact to upstream/downstream versions. For example, `frontend-v2` consumes `api-v2` and is validated by `test-v2`.
   Downstream technical/backend/frontend/testing versions must explicitly state which PRD/data-summary version and replacement rows they consume.

4. Record compatibility.
   Mark compatible, partial, breaking, deprecated, or blocked. Breaking changes must route to `$change-impact-analysis`.

5. Define release bundle.
   State exactly which artifacts belong in the current delivery package and which remain draft/obsolete.

6. Maintain index.
   Update the index after every approved change, test result, defect repair, or release. Do not overwrite history; append a new version row.

7. Link code file ledgers when code changes.
   For every scoped frontend/backend/prototype code file, apply `$code-change-ledger-management`, then link the sidecar ledger status and changed ranges in the delivery index.

## Script

Create a first-pass Markdown index:

```bash
python3 delivery-version-management/scripts/build_delivery_index.py <artifact-root> --out DELIVERY_INDEX.md
```

Use `--version release-v1` to stamp a target bundle version.

Create or append a per-code-file ledger:

```bash
python3 delivery-version-management/scripts/update_code_change_ledger.py --file <code-file> --stage before
python3 delivery-version-management/scripts/update_code_change_ledger.py --file <code-file> --stage after --summary "<change summary>" --ranges "L10-L42"
```

## Required Output

- Version chain: requirement/prototype/model/API/backend/frontend/test/release mapping.
- Delivery artifact index: artifact type, name, version, path, owner, status, upstream/downstream versions, change IDs, evidence.
- Prototype handoff version mapping when applicable: PRD execution bundle, `docs/prototype-data-summary.md`, replacement rows, metric/source/interface rows, component data keys, downstream consumer versions, and open `GAP-*`.
- Code file change ledger status when code changed: changed code file, sidecar ledger path, pre-change read evidence, appended version, changed code ranges, verification, and unresolved follow-up.
- Compatibility and freshness check: stale, missing, obsolete, breaking, partial, or ready.
- Release bundle: included artifacts, excluded drafts, required approvals, rollout/rollback notes.
- Follow-up actions: missing versions, required updates, owner workflows, and blockers.

## Quality Checklist

- Every delivery artifact has type, version, path/source, owner, and status.
- Version relationships are explicit and not inferred silently.
- Prototype-derived downstream artifacts are not version-complete unless PRD/data-summary consumption and replacement-row coverage are indexed.
- Test reports and automation runs point to the exact frontend/backend/API versions tested.
- Obsolete documents are marked obsolete rather than left ambiguous.
- Breaking or mismatched versions route to `$change-impact-analysis`.
- Frontend, backend, and runnable prototype code changes are not version-complete unless every changed scoped code file has a sidecar ledger that was read before edit and appended after edit with feature/code-range/version/verification information.
