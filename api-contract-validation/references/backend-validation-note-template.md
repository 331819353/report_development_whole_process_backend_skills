# Validation Note Template

Use this template for API contract validation output.

## Compact Template

- Endpoint or operation:
- Consumer/downstream:
- Compared artifacts:
- Runtime/source mode:
- Evidence:
- Entry consistency status:
- ENTRY findings:
- Design reasonableness status:
- DESIGN findings:
- Request command/tool:
- Environment and timestamp:
- Sample response or artifact path:
- Test command/result:
- Production readiness evidence:
- Runtime URL/health:
- API version/source alignment:
- Source replacement compatibility:
- Preserved response fields:
- Additive/new response fields:
- Breaking/deprecated response fields:
- Field naming/source-trace status:
- Observability/log evidence:
- Testing handoff:
- Contract status: pass / partial / fail / not tested
- Response field differences:
- Request/filter differences:
- Transformation sample results:
- Empty/error/auth results:
- Performance limits:
- Remaining missing information:

## Status Meaning

- `pass`: contract is consistent across the compared artifacts and tested/runtime evidence.
- `partial`: contract is usable but has documented assumptions, untested branches, unavailable sources, or limited evidence.
- `fail`: contract mismatch blocks reliable use or would break a consumer.
- `not tested`: endpoint or branch was in scope but no meaningful evidence could be collected.

For production-bound validation, `pass` also requires enough production-readiness evidence for the stated scope, including runtime URL/health, source mode, version alignment, auth/env behavior, observability or log traceability, performance/export limits, and testing handoff. Otherwise use `partial` or `not tested`.

## Evidence Rules

- Include a curl command, test command, browser/network capture, fixture path, log path, or response excerpt when a status relies on observed behavior.
- Redact secrets, tokens, credentials, cookies, and personally identifiable values.
- If evidence cannot be collected, use `not tested` or `partial` and record the blocker as a local `GAP-*` item with owner, impact, current assumption, and retest criteria.

## Failure Handling

- Fix mismatches immediately when they are local and low risk.
- Record absent facts as local `GAP-*` items with owner, impact, current assumption, and retest criteria.
- Record contradictory source artifacts through `ENTRY-*` findings from `$quality-gate-validation`; unresolved `P0`/`P1` findings block `pass` status for the affected operation and require user confirmation only before affected repairs.
- Record unreasonable contract shapes through `DESIGN-*` findings from `$quality-gate-validation`; unresolved `P0`/`P1` findings block pass status or keep the result partial.
- Record transformation mismatches as local transformation findings with source fields, target fields, rule gap, evidence, and affected contract status.
- For source/table/upstream/fixture replacement, record preserved fields, additive fields, naming/source-trace evidence, and any breaking/deprecated fields. A source replacement cannot pass when existing response fields drift without versioning and migration notes.
- Name the exact artifact that must change when the conflict is between documentation, frontend, backend, upstream, or tests.
