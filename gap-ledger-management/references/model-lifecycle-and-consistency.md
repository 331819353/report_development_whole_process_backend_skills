# Lifecycle And Consistency

Use this reference when updating gap status or keeping artifacts aligned.

## Status Values

- `open`: missing or ambiguous, no safe assumption yet.
- `assumed`: work can continue under an explicit assumption.
- `blocked`: downstream work cannot reliably continue.
- `resolved`: decision confirmed and affected artifacts updated.
- `obsolete`: no longer relevant because scope or design changed.

## Status Transition Rules

- `open` -> `assumed`: only when a safe fallback sentence is written.
- `open` -> `blocked`: when the missing item prevents reliable handoff.
- `assumed` -> `resolved`: only after confirmation source is recorded and artifacts are updated.
- `blocked` -> `resolved`: only after the blocker is answered and affected APIs/models are updated.
- Any status -> `obsolete`: only when the affected API/model/page is removed or replaced.

## Resolution Note

For resolved items, include:

- Decision.
- Date if known.
- Source of decision, such as data owner, business owner, requirement file, API doc, meeting note.
- Affected artifacts updated.

Example:

`Resolved: 使用不含税收入作为分母; confirmed by finance owner on 2026-06-01; updated MET-001, RSP-001, API-001.`

## Consistency Rules

- The same `GAP-*` ID must appear in API清单 and 数据模型文件 if both are affected.
- Assumption wording must be identical across affected artifacts.
- When a gap is resolved, remove `TBD` from the affected fields and update status from `partial` or `blocked` if appropriate.
- Do not leave resolved gaps in pending questions unless they are retained for audit history.
- When a requirement, interaction, or acceptance gap is resolved, update affected API清单 rows and technical-solution handoff notes, not only the gap ledger.
- When a security or performance gap is resolved, update affected data model fields, API permission/performance columns, and validation expectations.
