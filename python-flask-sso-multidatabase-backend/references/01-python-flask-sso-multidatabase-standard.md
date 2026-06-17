# Python Flask SSO And Multi-Database Backend Standard

Use this reference when a backend/data-service project uses Python as the primary language and needs Flask APIs, enterprise SSO, local/business/enterprise/analytics database access, report queries, or production-style deployment.

This standard complements `$backend-development-workflow` `references/report-data-service-backend-implementation.md`. That file governs report query-service behavior; this file governs the concrete Python/Flask project shape for SSO and multiple databases.

## Baseline Stack

Default backend stack:

```text
Python + Flask + SQLAlchemy + SSO + SQLite + MySQL + Oracle + StarRocks
```

Recommended supporting tools:

| Area | Default |
| --- | --- |
| HTTP framework | Flask with app factory and Blueprints |
| API style | RESTful API with versioned routes |
| Auth | Enterprise SSO, `Access-Token` request header, optional `Application-Key` when IAMA/clientId is in scope |
| DB access | SQLAlchemy engines/sessions plus parameter-bound SQL or ORM models |
| Local/test DB | SQLite |
| Business DB | MySQL |
| Enterprise/legacy DB | Oracle |
| Analytics/report DB | StarRocks through MySQL-compatible protocol |
| Cache/rate/session-like transient state | Redis when required and explicitly scoped |
| Async export/jobs | Celery or project-approved worker when heavy jobs exist |
| Tests | pytest |
| Runtime | Gunicorn + Nginx + Docker or project-approved equivalent |

Do not switch to FastAPI, Node, Spring, or another stack by default unless the user or existing project explicitly owns that choice.

## Architecture Boundary

Keep the backend layered:

```text
API/controller
-> middleware/auth/permission
-> service/use-case
-> repository/source adapter
-> db engine/session manager
-> SQLite/MySQL/Oracle/StarRocks
```

Rules:

- API/controller files stay thin: read request params, call schemas/validators, invoke service, return unified response.
- Service layer owns business orchestration, user/permission context, transaction boundary decisions, and calls to repositories.
- Repository layer owns SQL/ORM execution, database selection, parameter binding, dialect differences, and source-specific result conversion.
- `app/db/` owns engine/session creation, pool configuration, connection lifecycle, and safe shutdown.
- Complex SQL is stored under `app/sql/<db_name>/` when it is large, dialect-specific, or shared.
- Frontend must not send raw SQL, table names, database names, arbitrary operators, or permission scope.

## Recommended Directory Structure

Use this shape unless an existing project has an authoritative layout.

```text
app/
  __init__.py                  # Flask app factory
  config.py                    # env-driven config
  extensions.py                # db, redis, migrate, limiter, etc.
  response.py                  # unified response helpers
  exceptions.py                # error envelope and handlers
  api/
    __init__.py
    v1/
      __init__.py
      auth.py
      user.py
      report.py
      dashboard.py
  middlewares/
    auth_middleware.py         # SSO token validation
    permission_middleware.py   # business permission check
    rate_limit.py
  services/
    sso_service.py
    user_service.py
    permission_service.py
    report_service.py
    dashboard_service.py
  repositories/
    sqlite_repository.py
    mysql_repository.py
    oracle_repository.py
    starrocks_repository.py
    user_repository.py
  models/
    user.py
    role.py
    permission.py
  db/
    engines.py                 # multi-database engine registry
    sessions.py                # session/transaction helpers
    sql_loader.py              # optional SQL file loader
  schemas/
    user_schema.py
    report_schema.py
  utils/
    logger.py
    security.py
    pagination.py
    date.py
  sql/
    mysql/
    oracle/
    starrocks/
migrations/
tests/
logs/
scripts/
docs/
run.py
wsgi.py
requirements.txt
Dockerfile
docker-compose.yml
gunicorn.conf.py
nginx.conf
.env.development
.env.test
.env.production
README.md
```

## SSO Contract

The backend does not own username/password login when enterprise SSO is in scope.

Standard browser-to-backend request contract:

```http
Access-Token: <token>
Application-Key: <clientId>   # required when the IAMA/clientId contract is active
```

Rules:

- Read the token from the configured header, default `Access-Token`.
- If Haier IAMA/clientId is in scope, validate `Application-Key` before token check.
- Missing, empty, expired, malformed, invalid, or unverifiable token returns `401`.
- Valid token with insufficient business permission returns `403`.
- Frontend 401 behavior is re-login/retry-once; frontend 403 behavior is no-permission display.
- Backend protected APIs must validate tokens; frontend route hiding is not sufficient.
- Do not log raw tokens, cookies, SSO payloads, `Application-Key` secrets, or full user info payloads.
- Store only local user mapping, role, permission, org, and status fields required by the application. Do not store SSO passwords.

Recommended middleware flow:

```text
request
-> read Access-Token and optional Application-Key
-> validate token through SSO/IAMA service
-> map SSO account to local user
-> load role, org, permission, and data scope
-> attach current user/context to request
-> execute protected API
```

Required local user fields usually include:

- stable SSO account id;
- username/display name;
- employee number or email when needed;
- department/org fields when needed;
- active/disabled status;
- local roles and permission bindings.

## Multi-Database Responsibilities

Each database must have a declared role. Do not mix responsibilities casually.

| Database | Default role | Avoid |
| --- | --- | --- |
| SQLite | local development, lightweight fixture data, tests, demos | high-concurrency production, large analytics, core permission system |
| MySQL | users, roles, permissions, configs, forms, ordinary CRUD/business data | large multidimensional analytics when StarRocks/source OLAP is available |
| Oracle | enterprise core/legacy source integration, historical systems, existing business tables | using Oracle-specific logic as a hidden dependency for all report behavior without mapping |
| StarRocks | analytics, dashboards, reports, metrics, wide tables, aggregation queries | replacing transactional MySQL/Oracle semantics; mixed OLTP writes |

StarRocks may use a MySQL-compatible connection, but it remains an analytics database. Keep its SQL, function assumptions, transaction assumptions, and performance expectations separate from MySQL business SQL.

## Database Configuration

Use environment variables for every datasource. Do not commit real credentials.

```bash
SSO_VALIDATE_URL=
SSO_USER_INFO_URL=
SSO_TOKEN_HEADER=Access-Token
APPLICATION_KEY_HEADER=Application-Key

SQLITE_DATABASE_URL=sqlite:///./data/app.db
MYSQL_DATABASE_URL=mysql+pymysql://user:password@host:3306/app_db?charset=utf8mb4
ORACLE_DATABASE_URL=oracle+oracledb://user:password@host:1521/?service_name=orclpdb1
STARROCKS_DATABASE_URL=mysql+pymysql://user:password@host:9030/analytics_db?charset=utf8mb4

MYSQL_POOL_SIZE=
ORACLE_POOL_SIZE=
STARROCKS_POOL_SIZE=
DB_POOL_RECYCLE=3600
DB_POOL_PRE_PING=true
REDIS_URL=
LOG_LEVEL=INFO
```

Pool settings must be explicit for production-bound services. StarRocks pool size is especially important for report dashboards and export-heavy endpoints.

## Engine And Repository Rules

- Centralize engine creation in `app/db/engines.py` or equivalent.
- Use `pool_pre_ping`, recycle/timeout settings, and bounded pool size for real DBs.
- Use context managers or `try/finally` so every acquired connection/session is released on success, validation errors, `ApiError`, timeout, and generic exceptions.
- Use SQLAlchemy `text()` with bound parameters or ORM query APIs. Do not concatenate user values into SQL.
- Repositories return source rows or mapped records; services decide business composition.
- Keep dialect-specific SQL under database-specific repository or SQL directories.
- For report endpoints, push filters, permission scope, aggregation, sorting, pagination, Top N, and export scope into source/repository/precompute/cache, not frontend or in-memory post-filtering.

## Unified Response And Status Codes

Use one response envelope unless an existing project has a stronger convention:

```json
{
  "code": 200,
  "msg": "success",
  "data": {}
}
```

Status semantics:

| Status | Meaning | Frontend behavior |
| ---: | --- | --- |
| `200` | success | render data |
| `400` | invalid params | show validation message |
| `401` | missing/invalid/expired token | re-login/retry-once |
| `403` | valid identity but no permission | no-permission page/message |
| `404` | resource not found | show not-found/error state |
| `429` | rate limited | show retry/rate-limit message |
| `500` | backend error | show system error and keep request id |

The HTTP status and response `code` must not contradict each other for auth, permission, rate-limit, or server errors.

## Naming Rules

| Item | Rule | Example |
| --- | --- | --- |
| Python files/functions/variables | `snake_case` | `user_service.py`, `get_user_list` |
| Classes | `PascalCase` | `UserService` |
| Constants/env vars | `UPPER_CASE` | `SSO_VALIDATE_URL` |
| DB tables | `snake_case` | `user_role` |
| API path | REST-style, versioned | `/api/v1/users` |
| Permission code | `module:action` | `user:list` |
| SQL files | `snake_case` under database directory | `dashboard_metrics.sql` |

## Testing Requirements

- Use pytest for unit and API tests.
- Mock SSO token validation in unit tests; integration tests may use a controlled test SSO service or recorded safe contract.
- Test 401 missing/invalid token and 403 valid-token/no-permission separately.
- Use SQLite fixtures for local/mock-derived backend behavior, but do not treat JSON arrays or in-memory lists as the backend source.
- Add repository tests or integration smoke checks for each configured real database when production handoff depends on it.
- Add contract tests for API response shape, field names, units/precision, null behavior, pagination, filters, and source replacement compatibility.
- For StarRocks/report queries, include default and non-default filter cases, large result guardrails, timeout behavior, and connection release on failure.

## Deployment And Operations

Production-bound Python/Flask services need:

- `wsgi.py` entrypoint;
- Gunicorn worker/thread/timeout config;
- Nginx reverse proxy or project gateway contract;
- Dockerfile and environment profile separation;
- health/readiness endpoint;
- structured logging with request id and redaction;
- secret/config separation by environment;
- database pool, Redis pool, rate limit, timeout, retry, and fallback config;
- migration strategy for local MySQL/SQLite-owned application tables;
- deployment rollback and smoke-test commands.

## Readiness Blockers

Do not mark the backend standard or implementation `ready` when any of these are unresolved:

- SSO token header, validation endpoint, client/application key behavior, 401/403 boundary, or user mapping is undefined.
- Protected APIs rely only on frontend login state and do not validate tokens on the backend.
- Multiple databases are configured but their responsibilities, environment variables, pool settings, and repository owners are not declared.
- StarRocks is treated as ordinary MySQL without documenting analytics-only usage, SQL differences, transaction assumptions, and pool limits.
- Repository code can leak connections on exception paths.
- SQL uses string concatenation with user-controlled values.
- API controllers contain complex SQL/business logic instead of routing through service and repository layers.
- Secrets, tokens, raw SSO payloads, raw SQL literals, or raw personal data are logged.
- Tests do not cover auth failures, permission failures, non-default filters, source replacement compatibility, and at least one database-backed query path for the declared scope.
