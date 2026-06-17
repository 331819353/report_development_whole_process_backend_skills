---
name: haier-sso-integration
description: "[后端阶段] 本阶段版本仅服务后端/数据服务设计、API文档/契约、接口实现、运行验证和后端交付；不承接原型设计、前端代码或测试执行。用于海尔账号中心 IAM/IAMA 单点登录前后端接入。用户提到海尔IAM、海尔IAMA、账号中心、@haier/iam、window.__USERCENTER__、script版SSO、Application-Key、Access-Token、clientId、code换token、checkToken、JWT/session桥接、401重登、403无权限、logout、前后端SSO断点时触发。"
---

# Haier SSO Integration

## Stage Scope

Classification: 后端阶段.

Use this copy only inside the backend/data-service skill bundle. Treat frontend, prototype, and testing work as contracts, evidence, handoff notes, or blockers; do not edit those stages from this skill.

## Positioning

Use this skill to implement or review Haier account-center SSO across frontend and backend. It covers browser SDK/script integration, backend token exchange/checking, protected API middleware, and cross-end breakpoint handoff.

It does not replace generic runtime SSO testing; use `sso-auth-flow-test` when the task is to execute or evidence-test a running system.

## Reference Loading

- Frontend entrypoint selection: `references/frontend-integration-entrypoints.md`
- Frontend script SDK snippets and interceptors: `references/frontend-script-integration.md`
- Backend entrypoint selection: `references/backend-integration-entrypoints.md`
- IAMA API endpoints and response shape: `references/iama-sso-api.md`

## Anti-Laziness Gate

For non-trivial work, apply `$quality-gate-validation` `references/anti-laziness-execution-gate.md` before final output, handoff, or readiness. Do not mark the result ready while `LAZY-*` findings remain open, when available local evidence was not inspected, when owning skills were skipped, or when proof is limited to generic statements such as "checked", "optimized", "looks good", or "implemented".

## Workflow

1. Determine target side: frontend, backend, or full chain.
2. Identify runtime container: ordinary browser, static page, Vue/Vite app, iHaier/Feishu container, iframe/webview, backend service, middleware retrofit, or multi-tenant app.
3. Choose the integration path from the matching reference.
4. Define config: base URL, app/client ID, headers, token storage, callback URL, protected route/API scope, and logout behavior.
5. Implement or review the smallest project-native integration.
6. For cross-end failures, produce a breakpoint handoff with failing step, expected/actual behavior, frontend storage, request headers, backend status, and retest criteria.

## Required Output

- Chosen frontend/backend SSO path and reason.
- Config and environment variables needed.
- Files or modules to update.
- Auth header/token/session behavior.
- Frontend-facing login/tokenUrl response contract using `resultCode`, `resultMsg`, `access_token`, `expires_in`, `token_type`, `refresh_token`, and `account`.
- Token check ownership: frontend passes only `Access-Token` to the business backend; backend obtains configured `clientId` server-side and sends upstream `Application-Key`.
- 401, 403, logout, refresh, and deep-link behavior.
- Verification or breakpoint handoff.

## Quality Gate

- Do not mix script SDK and package SDK unless the project explicitly requires both.
- Do not hard-code secrets or tokens.
- Protected APIs must have backend validation, not only frontend hiding.
- Do not design login/tokenUrl responses with local aliases such as top-level `token`/`userInfo` as the primary contract; preserve the canonical IAMA fields shown above.
- Do not require the frontend to provide `Application-Key` or `clientId` for token check. Backend code must resolve the client ID from server-side config or a trusted tenant/app registry, then call IAMA check with that value and the frontend-provided `Access-Token`.
- 401 token invalid and 403 no-permission behavior must be distinct.
