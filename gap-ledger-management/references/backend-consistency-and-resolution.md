# Consistency And Resolution

Use this reference when maintaining missing-information items across code, docs, tests, and delivery artifacts.

## Consistency Rules

- Every temporary default in code must appear in the missing-information document with the same value and fallback behavior.
- Every documented assumption must match API docs, fixtures, tests, examples, and runtime behavior.
- Every contract mismatch found during backend contract validation should either be fixed or linked to a missing-information item.
- Every unknown transformation rule found during transformation design should either be resolved or linked to a missing-information item.
- Do not close an item only because it is mentioned in final prose; close it after the affected artifacts are updated.

## Resolution Workflow

1. Record the decision, source, owner, and date.
2. Update affected code, API docs, tests, fixtures, examples, deployment config, or validation notes.
3. Re-run the relevant focused validation when practical.
4. Change status to `resolved` and add a resolution log entry.

## Resolution Log Example

```markdown
- 2026-06-01: Product confirmed `status=archived` should be excluded by default. Updated API docs, service filter default, and contract test.
```

## Release Check

Before handoff or release, list all remaining `P0 blocked` and `P1 risky` items. State whether each item blocks delivery, limits scope, or is accepted as a temporary assumption.

## Aging And Escalation

- Give each `P0 blocked` and `P1 risky` item a due date or review date.
- Escalate overdue `P0` items to the delivery owner immediately.
- Escalate overdue `P1` assumptions before they become release blockers or user-visible behavior.
- Do not let an `assumed` item remain open indefinitely without a named owner and next review date.
