---
name: artifact-readability-standard
description: "[后端阶段] 本阶段版本仅服务后端/数据服务设计、API文档/契约、接口实现、运行验证和后端交付；不承接原型设计、前端代码或测试执行。用于设计或审计交付物是否同时便于人类评审和下游AI/自动化抽取。用户提到人和AI都可读、交付物结构、文档结构可复用、截图/图片如何转成AI可读规范、稳定ID、状态值、字段/接口/缺口/证据可抽取、不要AI式key-value墙、文档太难读、交付说明需要机器可读时触发；不替代具体API文档、测试报告或技术方案正文生成。"
---

# Artifact Readability Standard

## Stage Scope

Classification: 后端阶段.

Use this copy only inside the backend/data-service skill bundle. Treat frontend, prototype, and testing work as contracts, evidence, handoff notes, or blockers; do not edit those stages from this skill.

## Positioning

Use this skill to shape stage artifacts so business users, product owners, developers, testers, maintainers, and downstream AI agents can all understand and extract the same canonical contract.

It is a structure and readability standard. Load the owning domain skill for the content itself, such as API documentation, technical solution, frontend function description, test evidence, or data model mapping.

## Reference Loading

- Read `references/human-ai-readable-artifact-standard.md` before producing, restructuring, or accepting a dual-readable artifact.
- Read `references/visual-source-abstraction-standard.md` when screenshots, images, mockups, browser captures, or visual references must become reusable or AI-readable knowledge.

## Anti-Laziness Gate

For non-trivial work, apply `$quality-gate-validation` `references/anti-laziness-execution-gate.md` before final output, handoff, or readiness. Do not mark the result ready while `LAZY-*` findings remain open, when available local evidence was not inspected, when owning skills were skipped, or when proof is limited to generic statements such as "checked", "optimized", "looks good", or "implemented".

## Workflow

1. Identify artifact type, audience, downstream consumer, and canonical source of truth.
2. Decide whether one dual-readable artifact is enough or whether a human summary plus machine appendix is necessary.
3. Structure the output with human summary first, then source context, business/delivery flow, structured contract tables, decisions/gaps, verification, and optional schema appendix.
4. When visual sources are used, classify them as temporary evidence, exact restoration source, visual baseline, runtime asset, audit evidence, or reusable inspiration; convert reusable value into a text/structured visual pattern contract.
5. Preserve stable IDs, exact field names, endpoint paths, status values, owners, evidence, and linked gaps.
6. Check that tables support the narrative instead of replacing it.

## Required Output

- Artifact type and canonical source.
- Human-readable summary shape.
- Machine-extractable IDs, statuses, mappings, fields, endpoints, gaps, and evidence.
- For image/screenshot-derived material: source role, retention policy, extracted visual pattern, and whether a text-only downstream agent can use it.
- Section/table structure and appendix decision.
- Readiness: `ready`, `partial`, or `blocked`.

## Quality Gate

- Do not produce separate human and AI documents unless the relationship and canonical source are explicit.
- Do not leave opaque IDs without human labels or blocked/partial statuses without impact and next action.
- Do not use long AI-only key/value walls as the main artifact.
- Do not make raw screenshots or image vectors the only durable source of truth for reusable skill knowledge; extract text, layout, data, interaction, state, and acceptance rules.
