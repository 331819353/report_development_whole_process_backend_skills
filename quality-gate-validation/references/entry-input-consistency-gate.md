# Entry Input Consistency Gate

Use this gate before irreversible design, documentation, implementation, or repair when the entry materials contain more than one authority, such as user requirements, screenshots, HTML/source samples, API docs, API inventories, data model docs, metric lists, mock data, frontend/backend code, environment/auth notes, or runtime traces.

The goal is to catch logical loopholes and cross-document conflicts before the workflow repairs or builds on the wrong premise.

## When To Run

Run this gate when any of these are true:

- The user provides mixed entry materials, for example requirements plus HTML, API docs plus frontend code, or API docs plus data model files.
- A provided HTML/source sample, screenshot, mock dataset, API document, or source file appears to contradict the written requirement.
- A downstream stage would need to choose between competing meanings for a metric, filter, permission rule, API field, page module, data source, environment, or workflow scope.
- The task asks to repair, optimize, integrate, or replace data based on inherited artifacts whose authority is unclear.

If there is only one small input and no conflicting evidence, record `Entry consistency: not needed` and continue.

## Audit Workflow

1. Inventory entry materials.
   List each artifact, path or source name, version/date when known, role, and likely authority: user instruction, visual/sample authority, API/provider authority, data/source authority, implementation/runtime authority, or supporting evidence.

2. Extract comparable claims.
   Normalize claims into these slots: workflow scope, users, pages/modules, visible components, metrics, formulas, units, grain, filters, defaults, interactions, states, permissions, API endpoints, request params, response fields, data sources, freshness, ownership, environment/auth, and acceptance rules.

3. Compare authority pairs.
   Check at least these pairs when available:
   - Requirement vs HTML/screenshot/source sample.
   - Requirement vs API docs or API inventory.
   - HTML/mock/frontend view model vs API docs/provider samples.
   - API docs/API inventory vs data model/source docs.
   - API docs vs implemented routes or runtime traces.
   - Frontend function description vs API docs.
   - Auth/env notes vs frontend/backend implementation.

4. Classify findings.
   Use stable IDs such as `ENTRY-001`.

   - `P0 blocker`: conflicting delivery scope, authoritative source, P0 metric formula/grain, permission/auth rule, required API availability, destructive repair direction, or any conflict that would make implementation unreliable.
   - `P1 high`: major page/module/control, filter, drilldown, response-field, enum, date, unit, or state mismatch that changes user-visible behavior or adapter design.
   - `P2 medium`: non-core label, optional module, sample-only structure, minor display/default mismatch, or safely adaptable field difference.
   - `P3 low`: typo, wording, naming, or cosmetic mismatch with no contract impact.

5. Decide confirmation need.
   For unresolved `P0` and `P1` findings, do not invent a direction or silently repair the affected artifacts/code. Mark the affected scope `partial` or `blocked`, continue non-conflicting work, and ask for confirmation only for the exact disputed decision. `P2` and `P3` may be repaired with a visible assumption only when they do not change a core business, data, API, permission, or runtime contract.

6. Repair after confirmation.
   After the user confirms a direction, apply the same decision across all affected artifacts: requirement brief, prototype/source, binding matrix, API list, data model, API document, adapter mapping, tests, and handoff notes. If confirmation is unavailable, keep the same `ENTRY-*` ID open and finish with a `partial` or `blocked` handoff rather than waiting indefinitely.

## Confirmation Protocol

When `P0` or `P1` findings exist:

- Pause irreversible implementation or affected file edits only for the disputed scope.
- Present a compact conflict table with `ENTRY-*` ID, severity, conflicting sources, impact, proposed repair choices, and the single decision needed.
- Ask only the minimum confirmation questions needed to resolve the blocker.
- Continue non-conflicting discovery, baseline checks, case design, or handoff documentation when they do not bake in the disputed assumption.

If the user's current message already resolves the conflict explicitly, record that resolution and continue.

## Output Pattern

Use this compact output in task notes, handoff docs, or final responses when useful:

```text
Entry Consistency Audit
Artifacts: ...
Status: pass | partial | blocked | not needed
Findings:
- ENTRY-001 | P1 high | Requirement vs API docs | impact | proposed repair | confirmation needed
Decisions:
- ENTRY-001 resolved by user confirmation: ...
Assumptions:
- ...
```

## Pass Criteria

- Every material artifact has a role and authority.
- Conflicting claims are visible and classified.
- `P0` and `P1` conflicts are not silently repaired.
- Confirmed decisions are propagated to all downstream artifacts.
- Handoff readiness is not `ready` while unresolved `P0` or `P1` findings affect the next stage.
