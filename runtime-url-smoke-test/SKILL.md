---
name: runtime-url-smoke-test
description: "[后端阶段] 本阶段版本仅服务后端/数据服务设计、API文档/契约、接口实现、运行验证和后端交付；不承接原型设计、前端代码或测试执行。用于对已启动的前端/后端URL做基础冒烟验证。用户提到运行地址、访问地址、前端URL、后端URL、localhost、页面打不开、接口不通、健康检查、版本环境一致性、API base URL、proxy/CORS、静态资源、控制台错误、网络失败、先看能不能跑、冒烟测试时触发；不做深度联调用例执行。"
---

# Runtime URL Smoke Test

## Stage Scope

Classification: 后端阶段.

Use this copy only inside the backend/data-service skill bundle. Treat frontend, prototype, and testing work as contracts, evidence, handoff notes, or blockers; do not edit those stages from this skill.

## Overview

Use this skill at the start of the testing phase. It answers whether the provided running frontend URL and backend URL are reachable, aligned, and stable enough for deeper SSO, data consistency, and filter tests.

## References

- Use `$delivery-artifact-template-management` when the task needs a reusable URL smoke matrix/template or standardized evidence structure.
- Use `$environment-profile-contract` when the smoke result must prove test/production profile, API base URL, source mode, proxy/CORS, or mock isolation consistency.

## Required Inputs

- Running frontend URL.
- Running backend base URL, gateway URL, or representative API endpoint.

Optional inputs: environment name, expected version/build, API documentation, test account, known proxy/base path rules, source/Git diagnostics links.

## Anti-Laziness Gate

For non-trivial work, apply `$quality-gate-validation` `references/anti-laziness-execution-gate.md` before final output, handoff, or readiness. Do not mark the result ready while `LAZY-*` findings remain open, when available local evidence was not inspected, when owning skills were skipped, or when proof is limited to generic statements such as "checked", "optimized", "looks good", or "implemented".

## Workflow

1. Normalize runtime targets.
   Record the frontend URL, backend URL, protocol, host, port, base path, environment, and expected version if known.

2. Check reachability.
   Open the frontend URL and call the backend health endpoint or representative API. Record HTTP status, redirect behavior, response time, and whether a login redirect is expected.

3. Check frontend runtime basics.
   Confirm the page loads its main assets, router, CSS, JavaScript bundles, favicon/logo, and visible shell without blocking console errors.

4. Check backend runtime basics.
   Confirm the backend responds with the expected content type, error envelope, auth requirement, and no unexpected 5xx, gateway, CORS, or timeout failure.

5. Check frontend-to-backend wiring.
   Inspect browser network requests and verify API base URL, proxy path, path prefix, HTTPS policy, credentials mode, and CORS behavior match the environment.

6. Check version alignment.
   If version metadata is available, verify frontend build, backend build, API document, and optional source/Git commit refer to the same delivery under test.

7. Check environment profile consistency when in scope.
   Verify that the frontend URL, backend/API base URL, auth endpoint, source mode, and proxy/CORS behavior match the declared profile. If only one shared `.env` or production-to-test/mock wiring exists, route to `$environment-profile-contract`.

8. Decide test readiness.
   Continue only when the runtime pair is reachable and stable. If not, stop deeper testing and report the environment blocker with evidence.

## Required Output

- Frontend URL:
- Backend URL:
- Environment/version:
- Frontend load status:
- Backend health/API status:
- Console/network status:
- Proxy/CORS/base URL status:
- Readiness result: pass / fail / blocked
- Blockers:

## Pass Criteria

- Frontend URL opens in a browser and renders the expected shell.
- Backend URL or representative API is reachable and returns expected auth or data behavior.
- Browser network requests point to the intended backend environment.
- No blocking console, asset, CORS, proxy, gateway, or timeout errors prevent deeper testing.
