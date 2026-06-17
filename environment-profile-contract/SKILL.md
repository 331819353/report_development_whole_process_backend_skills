---
name: environment-profile-contract
description: "[后端阶段] 本阶段版本仅服务后端/数据服务设计、API文档/契约、接口实现、运行验证和后端交付；不承接原型设计、前端代码或测试执行。用于定义或审计跨前端、后端、测试、生产的环境Profile契约。用户提到环境Profile、.env.test、.env.production、测试生产隔离、API base URL与后端Profile对应、proxy/CORS/base path、生产不能指向mock/local/test、环境交付验收、配置契约、运行URL和Profile一致性时触发；不替代单个前端环境修复或URL冒烟。"
---

# Environment Profile Contract

## Stage Scope

Classification: 后端阶段.

Use this copy only inside the backend/data-service skill bundle. Treat frontend, prototype, and testing work as contracts, evidence, handoff notes, or blockers; do not edit those stages from this skill.

## Positioning

Use this skill when runtime delivery depends on explicit test and production environment contracts across frontend, backend, data source, auth, proxy/CORS, build, startup, smoke testing, and release acceptance.

Use `frontend-env-deployment-verification` for concrete frontend env/proxy/build repair. Use `$runtime-url-smoke-test` for reachability only.

## Reference Loading

- Read `references/environment-profile-contract.md` before accepting environment-sensitive handoffs, production readiness, or profile separation.

## Anti-Laziness Gate

For non-trivial work, apply `$quality-gate-validation` `references/anti-laziness-execution-gate.md` before final output, handoff, or readiness. Do not mark the result ready while `LAZY-*` findings remain open, when available local evidence was not inspected, when owning skills were skipped, or when proof is limited to generic statements such as "checked", "optimized", "looks good", or "implemented".

## Workflow

1. Identify deliverable runtime: frontend, backend/data service, integrated app, prototype, or release bundle.
2. Inventory required profiles: `.env.test` and `.env.production`, plus local/development convenience profiles when present.
3. Verify frontend test profile points to test backend/API, and production profile points to production backend/API.
4. Check auth/SSO endpoints, source mode, mock retention, proxy/CORS/base path, build/start commands, health/readiness, and version evidence.
5. Mark missing or unsafe profile decisions as blockers or partial readiness with owner action.

## Required Output

- Profile names and config files.
- Frontend URL, backend/API base URL, auth endpoint, source mode, proxy/CORS/base path, and command evidence.
- Mock/demo/local dependency status.
- Health/readiness or smoke evidence.
- Readiness: `ready`, `partial`, or `blocked`.

## Quality Gate

- Production-bound work is not ready with only one shared `.env`, unknown profile, or production values pointing to test/local/mock targets without owner approval.
- Do not expose secrets, tokens, passwords, private cookies, or personal account data.
