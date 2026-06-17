# Code File Change Ledger

Use this reference whenever frontend, backend, or runnable prototype code is created, modified, repaired, or refactored.

The goal is to make every code change traceable at file level, so later agents and engineers can quickly answer:

```text
Which feature does this file own?
Which code ranges changed in this iteration?
Why was the change made?
What exact lines changed?
Can the previous file state be reconstructed?
Which version introduced it?
How was it verified?
What should be checked before changing it again?
```

## Scope

Apply this ledger to source code files in frontend, backend, and prototype projects, including:

- UI/component code: `.vue`, `.tsx`, `.jsx`, `.ts`, `.js`, `.mjs`, `.css`, `.scss`, `.less`.
- Backend code: `.py`, `.java`, `.kt`, `.go`, `.ts`, `.js`, `.sql` when it owns service behavior.
- Configuration code that changes runtime behavior: route config, dashboard config, API client config, data-source registry, middleware config, build/runtime config.
- Test code when the test itself is changed as part of a feature or defect fix.

Exclude generated build output, lockfiles, dependency folders, binary files, screenshots, large fixture data, and third-party vendored code unless the project explicitly treats them as maintained source.

## Ledger Location

Default location is a sidecar Markdown file in the same directory as the code file:

```text
<code-file-directory>/__change_logs__/<code-file-name>.changes.md
```

Examples:

```text
src/widgets/components/SalesTrend.vue
src/widgets/components/__change_logs__/SalesTrend.vue.changes.md

backend/routes/report_api.py
backend/routes/__change_logs__/report_api.py.changes.md
```

If an existing project already has a stricter file-level change ledger convention, use the project convention only when it still supports per-code-file traceability, pre-change reading, post-change append, version history, and changed code ranges.

## Required Trigger Behavior

Before changing a scoped code file:

1. Locate the ledger file for that code file.
2. If it does not exist, create it from the current file baseline before editing.
3. Read the ledger before deciding the edit.
4. Use the existing feature inventory, known ranges, risks, and prior version notes to avoid overwriting intended behavior.

After changing the code file:

1. Append a new version entry to the same ledger.
2. Record the functional change, changed code range, version, verification, rollback notes, and reversible change evidence.
3. Do not overwrite previous entries.
4. If line numbers moved, record both old range when known and new range after the edit.
5. Treat a sha256 as an integrity checksum only. It cannot identify changed lines or reconstruct prior content.

This is required even for small fixes when they touch frontend, backend, or prototype source code.

## Minimum Ledger Structure

Each ledger should contain:

```markdown
# Code Change Ledger: <relative-code-file-path>

- Code file: `<relative-code-file-path>`
- Ledger file: `<relative-ledger-path>`
- Purpose: <what this file owns>
- Primary features: <feature list or TBD>
- Last reviewed before edit: <timestamp / version / actor>

## Functional Inventory

| Feature ID | Feature / Behavior | Main Code Range | Inputs | Outputs | Notes |
| --- | --- | --- | --- | --- | --- |

## Version Entries

### <version> - <timestamp>

- Change ID:
- Actor:
- Change type: create / update / repair / refactor / test / config
- Summary:
- Modified functionality:
- Code ranges:
- Modified content:
- Affected contracts:
- Verification:
- Rollback note:
- Related files:
- Before snapshot:
- After snapshot:
- Change evidence:
- Follow-up:
```

## Required Fields For Each Version Entry

| Field | Requirement |
| --- | --- |
| `version` | Use project release version, branch/commit, requirement/change ID, or generated timestamp version such as `v20260611-143012` when no version exists yet. |
| `change ID` | Use issue/requirement/defect ID when available; otherwise write `ad-hoc` with a short reason. |
| `summary` | One sentence explaining the user-facing or service-facing change. |
| `modified functionality` | Feature list, behavior list, or affected function/component/API route names. |
| `code ranges` | New line ranges after the edit, and old ranges when known. Use `L10-L42`, `function buildQueryContext`, `component <template> filter area`, or equivalent stable anchors. |
| `modified content` | What changed technically: data binding, layout, API call, validation, adapter, logging, error handling, tests, etc. |
| `affected contracts` | API fields, props, emitted events, env vars, filters, permission scope, logging fields, data model fields, or `none`. |
| `verification` | Commands, browser checks, API smoke checks, unit tests, lint/build, or `not run` with a precise blocker. |
| `rollback note` | How to undo safely or what dependency must be reverted together. |
| `before snapshot` | Previous state evidence: line count plus sha256 from the pre-edit snapshot, or external VCS/release reference. |
| `after snapshot` | New state evidence: line count plus sha256 after the edit. |
| `change evidence` | Inline unified diff, sidecar patch path plus sha256, or exact external VCS commit/diff reference. Hash-only evidence is insufficient. |

## Code Range Rules

- Prefer stable function/component/route names plus line ranges.
- For Vue single-file components, separate `<template>`, `<script setup>`, and `<style scoped>` when all are touched.
- For backend route/service files, record route path, service function, repository function, and middleware hook when relevant.
- For SQL or query-builder code, record the query name, metric/source mapping, parameter predicate, and guardrail range.
- When a formatter moves line numbers, update the new range after formatting.
- Do not use `full file` by itself for ordinary source changes. If the entire file was replaced, still record the top-level sections that changed and attach a unified diff or sidecar patch.
- For structured files such as `package.json`, `tsconfig.json`, route registries, env schemas, and dashboard configs, add section anchors such as `scripts`, `dependencies`, `compilerOptions`, `routes[]`, or `screen.layout`, plus changed line ranges when available.

## Reversible Evidence Rules

Use the lowest-friction evidence that lets a later agent or engineer understand and undo the change:

1. Prefer an inline unified diff for normal text code files.
2. Use a sidecar patch file under the same `__change_logs__` directory only when the diff is too large for readable inline ledger content. Record its relative path and sha256.
3. Use an external VCS commit, tag, or release bundle only when it is available and named precisely enough to recover both before and after content.
4. For binary, generated, large fixture, or vendored files that are intentionally excluded from ledger scope, record the exclusion reason instead of pretending sha256 is a complete change record.

Hash-only entries are never enough for readiness:

```text
File snapshot: 37 lines, sha256 `...`
```

This proves only that the current file matches a recorded state. It does not show what changed and cannot reconstruct the previous state.

## Creation And Update Script

Prefer the bundled helper when available:

```bash
python3 delivery-version-management/scripts/update_code_change_ledger.py \
  --file <path-to-code-file> \
  --stage before

python3 delivery-version-management/scripts/update_code_change_ledger.py \
  --file <path-to-code-file> \
  --stage after \
  --summary "<what changed>" \
  --features "<feature/function list>" \
  --ranges "L10-L42, L88-L104" \
  --modified-content "<technical change>" \
  --verification "<commands or blocker>"
```

In copied prototype templates, use the local npm wrapper when present:

```bash
npm run ledger:code -- --file src/widgets/components/SalesTrend.vue --stage before
npm run ledger:code -- --file src/widgets/components/SalesTrend.vue --stage after --summary "..." --ranges "L10-L42"
```

The helper should be run in both stages. `before` captures a pre-edit snapshot; `after` compares the snapshot with the edited file and appends a unified diff or sidecar patch. If the helper reports that no pre-edit snapshot exists, the ledger entry is not ready unless an exact external VCS/release reference is supplied.

Manual updates are acceptable when the project does not run Python/Node, but the same fields and before/after behavior still apply.

## Quality Gate

Do not mark code implementation, repair, or prototype delivery `ready` when any scoped changed code file lacks:

- a sidecar ledger file;
- evidence that the ledger was read before editing;
- a post-change version entry;
- changed code ranges or stable anchors;
- unified diff, sidecar patch, or exact external VCS/release reference;
- functional summary and affected contracts;
- verification or a precise blocker.

The following patterns fail readiness:

- `Code ranges: full file` with no section anchors or diff.
- `Verification: sha256 ...` or `File snapshot: ... sha256 ...` as the only change evidence.
- `Rollback note: use VCS history` when the target directory is not a VCS checkout or the exact commit/tag is not named.
- `Modified content: standard refactor` without listing changed sections, dependencies, routes, props, fields, or behavior.

Do not bury this information only in a final chat message, commit message, PR description, or broad delivery index. Those are useful summaries, but they do not replace file-level ledgers.
