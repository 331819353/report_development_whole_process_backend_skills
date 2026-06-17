---
name: permission-matrix-validation
description: "[后端阶段] 本阶段版本仅服务后端/数据服务设计、API文档/契约、接口实现、运行验证和后端交付；不承接原型设计、前端代码或测试执行。用于企业报表权限矩阵设计、权限验收和多角色测试。用户提到权限矩阵、角色权限、组织/区域/门店/供应商/管理员视角、多角色验收、菜单权限、页面权限、字段可见性、数据范围、操作权限、导出权限、脱敏、行级/列级权限测试时触发；不负责通用SSO接入。"
---

# Permission Matrix Validation

## Stage Scope

Classification: 后端阶段.

Use this copy only inside the backend/data-service skill bundle. Treat frontend, prototype, and testing work as contracts, evidence, handoff notes, or blockers; do not edit those stages from this skill.

## Overview

Use this skill to design and validate role-based access for enterprise reports. It produces a role x page x field x action x data-scope x export matrix and corresponding acceptance cases.

## Inputs

- Role list, organization hierarchy, page list, API docs, data model, field sensitivity, SSO/auth notes, export rules, screenshots, or known permission defects.
- Optional: test accounts, org codes, sample data ownership, environment URL, audit requirements, and legal/security policy.

Use `$delivery-artifact-template-management` when producing a reusable permission matrix.

## Anti-Laziness Gate

For non-trivial work, apply `$quality-gate-validation` `references/anti-laziness-execution-gate.md` before final output, handoff, or readiness. Do not mark the result ready while `LAZY-*` findings remain open, when available local evidence was not inspected, when owning skills were skipped, or when proof is limited to generic statements such as "checked", "optimized", "looks good", or "implemented".

## Workflow

1. Define roles and scopes.
   Capture role, organization level, data scope, inherited permissions, exclusions, and test accounts.

2. Define protected surfaces.
   List menu, route/page, component, KPI, chart, table field, drawer/detail, operation, export/download, API endpoint, and data row scope.

3. Build matrix.
   For every role/surface, state visible/hidden, editable/read-only, allowed/denied, masked/unmasked, exportable/not exportable, and API access expectations.

4. Define test cases.
   Include positive, negative, cross-role, deep-link, API direct-call, export, no-permission, expired token, and data boundary cases.

5. Validate runtime when possible.
   Use test accounts and URLs to verify UI visibility, API response filtering, export contents, no-permission states, and audit evidence. Route SSO/token flow to `sso-auth-flow-test`.

6. Report gaps.
   Missing accounts, unclear org scope, undocumented field sensitivity, or inconsistent frontend/backend permission behavior must be blockers.

## Required Output

- Role and organization model.
- Permission matrix: role x page/menu/component/field/action/data scope/export/API.
- Multi-role test matrix: case ID, account/role, action, expected UI/API/export behavior, evidence, status.
- Runtime result when executed: screenshots, API samples, export samples, console/network notes.
- Defects/blockers: category, severity, likely owner, reproduction steps, retest criteria.
- Downstream handoff to API/model/frontend/testing/version workflows.

## Quality Checklist

- Data range, field visibility, operation permission, and export permission are all explicit.
- Backend/API filtering is validated separately from frontend hiding.
- Deep-link and direct API access are covered for denied roles.
- Export/download inherits active role and data-scope restrictions.
- No role is marked accepted without an account or documented reason for not running.
