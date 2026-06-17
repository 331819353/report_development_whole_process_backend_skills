# Anti-Laziness Execution Gate

Use this gate to prevent shallow execution: starting without enough evidence, taking the convenient implementation path, skipping owning skills, or declaring `ready` without proof.

Load this gate for non-trivial implementation, repair, QA, acceptance, handoff, or any task that has previously failed due to missed constraints.

## Required Checks

| Check | Required evidence |
| --- | --- |
| Evidence-first | List the local/source evidence inspected before making a decision: files, screenshots, runtime URL, logs, API samples, config, ledgers, docs, or command output. |
| Local evidence exhausted | Inspect available local evidence before asking the user or guessing. Ask only when an unresolved P0/P1 decision remains. |
| Owning skill used | Name each affected surface and the specific owning skill loaded for it. Broad workflows alone are not enough for chart/table/filter/layout/API/runtime defects. |
| Decision log | For hard choices, record decision, evidence, rejected alternative, and acceptance impact. Hard choices include template, renderer, source authority, writable target, data/API path, chart/table type, layout canvas, and whether to preserve sample style. |
| Before/after proof | For repairs or optimizations, state the before problem, the changed behavior, and the after evidence that proves the issue is fixed or still partial. |
| No proof, no ready | `ready` requires concrete evidence: file/line or stable anchor, command, screenshot/crop, DOM check, API response, diff, ledger entry, or test result. Without proof, use `partial`. |
| Executable proof obligations | For visual/layout/component contracts, list the required proof obligations and bind each one to at least one executable or inspectable proof: DOM selector/semantic role, computed CSS/cascade check, ECharts/S2 option/config field, browser geometry assertion, screenshot/crop, or source line. |
| Rule strength audit | Classify normative rules as `MUST/fail`, `SHOULD/exception-required`, or `MAY/optional`. Any rule that affects correctness, data trust, renderer ownership, filter scope, permission/export/query behavior, runtime layout fit, accessibility, or readiness evidence must be `MUST/fail` with a testable proof. |
| Regression probe | Before final readiness, ask what the change could have broken, then verify or record the unverified risk. |
| Output completeness | Required outputs from the owning skill are present. Missing preflight, action reflection, code ledger, runtime QA, or specialized acceptance proof downgrades readiness. |

## Lazy Smells

Treat these as `LAZY-*` findings. They block `ready` unless an explicit scoped exception is accepted.

| ID | Smell | Why it blocks |
| --- | --- | --- |
| `LAZY-EVIDENCE-THIN` | Gives a conclusion after reading only a top-level file, prompt, or screenshot while relevant local evidence exists. | The conclusion may be based on a convenient subset of evidence. |
| `LAZY-SKILL-SKIP` | Uses only a broad workflow when a specific owning skill is triggered by the affected surface. | Specialty constraints are likely missed. |
| `LAZY-ASK-BEFORE-INSPECT` | Asks broad user questions before inspecting local files, configs, logs, screenshots, or docs that could answer them. | User clarification becomes a substitute for basic discovery. |
| `LAZY-GUESS-AUTHORITY` | Does not decide which source wins when requirement, HTML/sample, code, API, data, or runtime evidence disagree. | Implementation may follow the easiest source rather than the authoritative one. |
| `LAZY-DEFAULT-PATH` | Chooses template, renderer, stack, data source, or layout because it is convenient, without evidence and rejected alternatives. | Convenience replaces design or engineering judgment. |
| `LAZY-IMPORT-ONLY` | Treats dependency import/install as implementation proof, such as importing ECharts while rendering manual chart marks. | The required engine behavior is not actually implemented. |
| `LAZY-SCREENSHOT-ONLY` | Uses screenshots alone for runtime/visual readiness when DOM, source, console, network, or component crops are required. | Hidden overflow, stale data, collisions, or renderer issues can pass unnoticed. |
| `LAZY-DEFAULT-STATE-ONLY` | Tests only default state and skips non-default filters, perspective switches, empty/error/no-permission, or long-label/dense-data states. | User workflows and edge states remain unverified. |
| `LAZY-SURFACE-FIX` | Fixes surface CSS/layout without checking data contract, component internals, renderer ownership, or downstream side effects. | The visible symptom may move while the defect remains. |
| `LAZY-READY-WITHOUT-PROOF` | Claims done/ready without concrete after evidence, command output, screenshot, ledger, diff, or test result. | The readiness state cannot be audited. |
| `LAZY-LEDGER-SHA-ONLY` | Records only commit/sha/version without changed ranges, diff, before/after snapshot, or rollback evidence. | The change is not reversible or reviewable from the ledger. |
| `LAZY-HTML-COPY` | Copies HTML/sample SVG/canvas/DOM chart marks into standard chart implementation instead of rebuilding data-driven ECharts/S2/project components. | Sample restoration overrides renderer and data-binding constraints. |
| `LAZY-CONTRACT-THEATER` | Declares contracts such as `compositePanelContract`, `analysisInsightContract`, KPI placement rules, or control metadata, but cannot point to matching DOM attributes/classes, CSS implementation, ECharts/S2 options, browser assertions, or screenshot/crop evidence. | The artifact is compliant in prose/config but not enforceable in runtime behavior. |
| `LAZY-ADVISORY-AS-PASS` | Treats advisory wording such as should/recommended/prefer/default/建议 as enough for readiness when the rule affects correctness, data trust, runtime fit, renderer ownership, filter scope, permission/export/query behavior, or accessibility. | A soft recommendation lets a required constraint pass without proof. |

## Readiness Rules

- `ready`: no blocking `LAZY-*` findings remain, and every required owning-skill output has evidence.
- `partial`: work is useful but lacks one or more proofs, non-default states, runtime evidence, specialized skill checks, or regression probes.
- `blocked`: the next action would require guessing source authority, data contract, permission, renderer, runtime target, or acceptance basis.

## Required Output

When this gate is used, include:

- Evidence inspected.
- `LAZY-*` findings or explicit no-finding result.
- Hard decisions and rejected alternatives.
- Before/after proof for fixes.
- Proof obligations with pass/fail evidence for any visual/layout/component contract.
- Rule strength audit for standards or specs that contain advisory wording in high-risk areas.
- Regression probe result.
- Final readiness: `ready`, `partial`, or `blocked`.

## Quality Gate

- Do not downgrade this gate to a prose reminder. If a lazy smell is present, emit a `LAZY-*` finding with owner and required action.
- Do not mark `ready` by saying "checked" or "looks good"; cite the actual evidence.
- Do not let broad workflow completion hide missing specialized skill acceptance.
