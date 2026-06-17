---
name: python-flask-sso-multidatabase-backend
description: "[后端阶段] 本阶段版本仅服务后端/数据服务设计、API文档/契约、接口实现、运行验证和后端交付；不承接原型设计、前端代码或测试执行。用于按 Python + Flask + SQLAlchemy + SSO 单点登录 + 多数据库适配沉淀后端项目架构、目录结构、认证鉴权、数据库连接和工程约定。用户提到 Python后端、Flask后端、项目目录结构、SQLAlchemy、Access-Token、Application-Key、401/403、SQLite/MySQL/Oracle/StarRocks、多数据库适配、Repository/Service、Gunicorn/Nginx/Docker、pytest、按样例开发后端接口或数据服务时触发。"
---

# Python Flask SSO Multi-Database Backend

## Stage Scope

Classification: 后端阶段.

Use this copy only inside the backend/data-service skill bundle. Treat frontend, prototype, and testing work as contracts, evidence, handoff notes, or blockers; do not edit those stages from this skill.

## Positioning

Use this skill as the architecture baseline for Python backend development when the project should follow a Flask + SQLAlchemy + enterprise SSO + multi-database structure.

It complements `$backend-development-workflow`: load this skill when the backend target should follow the Python/Flask architecture, SSO token validation, SQLite/MySQL/Oracle/StarRocks role split, repository/service layering, and deployment conventions. Use `$haier-sso-integration` for Haier IAM/IAMA endpoint details, `$api-documentation-design` for formal API docs, and `$performance-optimization` for SQL/cache/pool tuning.

## Reference Map

| Need | Read |
| --- | --- |
| Stack, directory structure, SSO, database roles, engine/session rules, response/status, naming, tests, deployment, readiness blockers | `references/01-python-flask-sso-multidatabase-standard.md` |

## Anti-Laziness Gate

For non-trivial work, apply `$quality-gate-validation` `references/anti-laziness-execution-gate.md` before final output, handoff, or readiness. Do not mark the result ready while `LAZY-*` findings remain open, when available local evidence was not inspected, when owning skills were skipped, or when proof is limited to generic statements such as "checked", "optimized", "looks good", or "implemented".

## Workflow

1. Confirm whether the target is a new Python/Flask backend, an existing sample-like backend, a migration into this architecture, or a repair.
2. Inspect existing stack. Prefer the standard stack when no authoritative override exists: Python, Flask, SQLAlchemy, SSO, SQLite for local/test, MySQL for business/user/permission/config, Oracle for enterprise legacy/core sources, StarRocks for analytics/report queries, Redis when needed, pytest, Gunicorn/Nginx/Docker for deployment.
3. Align directories and ownership: `app/api`, `app/middlewares`, `app/services`, `app/repositories`, `app/models`, `app/db`, `app/schemas`, `app/utils`, and `app/sql/<db_name>`.
4. Define SSO behavior: `Access-Token`, optional `Application-Key` when IAMA/clientId is active, token validation owner, local user-role-permission mapping, 401 token-invalid behavior, and 403 permission-denied behavior.
5. Define the multi-database role map and SQLAlchemy engine/session lifecycle before repository implementation.
6. Keep controllers thin. Put token validation in middleware/service, business orchestration in services, and database access in repositories/source adapters.
7. Define env variables, secret handling, response envelope, error/status mapping, logging/redaction, tests, WSGI/Gunicorn/Docker/Nginx or gateway entrypoints.
8. Route API contract, report query-service, performance, SSO endpoint details, or runtime smoke work to the owning skills when the task goes beyond architecture baseline.

## Required Output

- Target backend mode: new, existing sample-like, migration, or repair.
- Stack and override decision.
- Directory/file plan with ownership layer.
- SSO/auth plan: headers, validation path, local user mapping, 401/403 behavior, redaction.
- Multi-database plan: SQLite/MySQL/Oracle/StarRocks roles, env vars, engine/session ownership, pool settings, SQL directory split.
- API/service/repository/db layering plan.
- Response/status, naming, testing, deployment, and readiness notes.
- Handoff notes for `$backend-development-workflow`, `$api-documentation-design`, `$haier-sso-integration`, `$performance-optimization`, or `$runtime-url-smoke-test` when needed.

## Quality Gate

- Do not treat Python/Flask as just a route file plus SQL strings; layer API, middleware, service, repository, db, schema, and utility responsibilities.
- Do not mark protected APIs ready when backend token validation, 401/403 split, or local user/permission mapping is missing.
- Do not treat StarRocks as ordinary MySQL; its analytics role, SQL assumptions, transaction assumptions, pool settings, and performance limits must be explicit.
- Do not mix database responsibilities without a role map.
- Do not concatenate user-controlled values into SQL.
- Do not allow repository or export paths to leak pooled connections on exceptions.
- Do not log raw tokens, SSO payloads, secrets, raw SQL literals, or raw personal data.
- Do not claim architecture alignment until directory placement, SSO behavior, database ownership, env/profile strategy, test scope, and deployment entrypoints are explicit.
