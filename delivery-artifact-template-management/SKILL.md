---
name: delivery-artifact-template-management
description: "[后端阶段] 本阶段版本仅服务后端/数据服务设计、API文档/契约、接口实现、运行验证和后端交付；不承接原型设计、前端代码或测试执行。用于管理报表交付物模板和标准矩阵结构。用户提到数据模板、交付模板、API清单模板、API文档模板、数据模型模板、权限矩阵、质量规则、测试矩阵、筛选联动矩阵、筛选前数据完整性模板、缺陷证据模板、功能说明模板、版本索引模板、统一文档骨架、可复用表格结构时触发；不负责填充具体业务内容。"
---

# Delivery Artifact Template Management

## Stage Scope

Classification: 后端阶段.

Use this copy only inside the backend/data-service skill bundle. Treat frontend, prototype, and testing work as contracts, evidence, handoff notes, or blockers; do not edit those stages from this skill.

## Positioning

Use this skill when the deliverable is a reusable artifact template, matrix schema, or document skeleton. It keeps artifact formats centralized so workflows and atomic skills do not each invent their own table columns.

It does not fill the template with final business/API/model/test content unless another skill supplies the content.

## Reference Library

Available template references:

- `references/api-inventory-template.md`
- `references/api-document-structure.md`
- `references/data-model-file-template.md`
- `references/data-quality-rule-template.md`
- `references/permission-matrix-template.md`
- `references/integration-test-case-matrix-template.md`
- `references/test-evidence-defect-template.md`
- `references/delivery-index-template.md`
- `references/frontend-function-document-structure.md`
- `references/filter-linkage-matrix-template.md`
- `references/data-consistency-matrix-template.md`
- `references/url-smoke-matrix-template.md`
- `references/sso-case-matrix-template.md`
- `references/automation-test-matrix-schema.md`

## Anti-Laziness Gate

For non-trivial work, apply `$quality-gate-validation` `references/anti-laziness-execution-gate.md` before final output, handoff, or readiness. Do not mark the result ready while `LAZY-*` findings remain open, when available local evidence was not inspected, when owning skills were skipped, or when proof is limited to generic statements such as "checked", "optimized", "looks good", or "implemented".

## Workflow

1. Identify the artifact type and downstream consumer.
2. Load only the matching template reference.
3. Preserve required IDs, status values, ownership fields, evidence columns, and readiness values.
4. If composing multiple templates, keep them linked through stable artifact IDs rather than merging unrelated tables.
5. Return the template, required fields, optional fields, examples, and validation checklist.

## Required Output

- Template name and use case.
- Required columns/sections.
- Optional columns/sections.
- Status values and ID conventions.
- Handoff and validation notes.

## Quality Gate

- Do not merge unrelated artifact types into one over-broad table.
- Do not drop traceability, owner, evidence, status, or blocker fields.
- Templates should be human-readable and machine-extractable.
