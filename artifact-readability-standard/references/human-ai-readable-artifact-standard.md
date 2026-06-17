# Human And AI Readable Artifact Standard

Use this standard for every stage artifact that may be read by business users, product owners, developers, testers, maintainers, or downstream AI agents.

## Default Decision

Produce one dual-readable artifact by default.

Do not create separate "human version" and "AI version" documents unless one of these is true:

- the user explicitly requests separate documents;
- an external formal deliverable needs narrative formatting while implementation needs a strict machine schema;
- the machine-readable section is too large for the human document and would make review difficult;
- audit, compliance, procurement, or release governance requires a separate appendix/package.

When separate outputs are necessary, keep one canonical source of truth and name the relationship clearly, such as "Human Summary consumes Contract Appendix v1.2". Do not let two documents drift.

## Required Shape

A dual-readable artifact should use this order unless a specialized template overrides it:

1. Human summary
   - 3-7 bullets or short paragraphs.
   - State purpose, scope, key decisions, readiness, and blockers in plain language.
2. Scope and source context
   - List input sources, version/commit/date when known, and which source is authoritative.
3. Main content by business or delivery flow
   - Explain what is being delivered, why it matters, and how people will use or validate it.
   - Use business names before technical IDs.
4. Structured contract tables
   - Preserve stable IDs, field names, endpoint paths, component IDs, status values, owner, evidence, and linked gaps.
   - Tables must be understandable without reading code.
5. Decisions, assumptions, and gaps
   - Keep `ENTRY-*`, `DESIGN-*`, `GAP-*`, `MI-*`, defect IDs, and readiness values stable.
   - Every blocker needs impact, owner/source needed, and next action.
6. Verification and handoff
   - Include commands, URLs, screenshots/logs, runtime evidence, test scope, readiness, and next-stage consumer.
7. Optional machine-readable appendix
   - Use when JSON/YAML/OpenAPI/schema-like content is useful.
   - Keep large raw schemas, sample payloads, and generated matrices out of the main narrative when they hurt readability.

## Writing Rules

- Start each major section with a human-readable sentence before tables.
- Prefer Chinese business labels for headings and descriptions; keep technical IDs in monospace beside them.
- Avoid long AI-only key/value walls in the main body. Convert them into concise tables plus short explanations.
- Keep tables narrow. If a table needs more than 8-10 columns, split it into overview + details, or move raw details to an appendix.
- Every ID must have a human label or description. Do not leave rows that only contain opaque IDs.
- Every status must explain impact. `partial` and `blocked` are not enough by themselves.
- Use examples sparingly in the main body; put exhaustive examples in appendices.
- Keep JSON/YAML/code blocks only for real contracts, payload examples, commands, or config snippets. Do not use them as the primary explanation.
- Use stable field names and exact enum/status values so downstream AI can extract the contract.
- Link related artifacts by path/version/commit when known.

## Artifact-Specific Guidance

- Requirement and prototype artifacts: open with business question, target users, page/module scope, and key visual/data decisions; then provide binding matrix and mock/filter/interaction contracts.
- Technical-solution artifacts: open with business goal, architecture blueprint, technology selection/ADR, implementation roadmap, runtime/security/production-readiness decisions; then provide API清单, 数据模型文件, gap/risk ledger, and readiness tables.
- API documentation: open with conventions and endpoint overview; keep endpoint details structured, but summarize each endpoint's purpose and consumer before schemas.
- Frontend function descriptions: open with pages and user workflows; then list feature inventory, provider mapping, filters, interactions, states, verification, and known limitations.
- Data-service/backend artifacts: open with service boundary, layered architecture, query-service chain, runtime/security/observability decisions, and readiness; then list API families/routes, transformations, auth, errors, health, logs, deployment, and operational notes.
- Testing artifacts: open with test objective and verdict; then provide case matrix, evidence, defects, retest criteria, and readiness.

## Quality Gate

Before final handoff, check:

- A human reader can understand scope, decisions, readiness, and next action in the first screen or first section.
- A downstream AI can extract stable IDs, statuses, mappings, fields, endpoints, gaps, and evidence without guessing.
- Main sections are organized by business flow or delivery stage, not by internal model thoughts.
- Tables and appendices support the narrative instead of replacing it.
- There is one canonical truth for each contract. If separate human/machine files exist, their version relationship is explicit.
