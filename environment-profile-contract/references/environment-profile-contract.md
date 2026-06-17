# Environment Profile Contract

Use this shared contract whenever a data service, data-visualization frontend, runtime URL, deployment note, or production-readiness handoff depends on environment configuration.

The delivery pipeline must distinguish test and production runtime profiles. A single undifferentiated `.env` file is not enough for data-service or data-visualization delivery.

## Required Profiles

Each deliverable runtime must define these two profile files:

- `.env.test`: test, integration, UAT, or staging-like runtime values.
- `.env.production`: production runtime values.

`.env.local`, `.env.development`, or a plain `.env` may exist for developer convenience, but they do not replace `.env.test` or `.env.production` for handoff, integration testing, or release acceptance.

If real values are sensitive, keep committed examples such as `.env.test.example` and `.env.production.example`, and provide the real runtime files through the project's secret/config channel. Do not commit tokens, passwords, private cookies, or personal account data.

## Profile Separation Rules

- The data service and the data-visualization frontend must each record which profile is used for build, startup, preview, smoke testing, integration testing, and production acceptance.
- Test and production values must not silently share API hosts, database/source locators, SSO/auth endpoints, credentials, logging destinations, feature flags, or source modes. If a value is intentionally shared, document the owner-approved reason.
- The frontend test profile must point to the test backend/API profile. The frontend production profile must point to the production backend/API profile.
- Local proxy settings must be profile-aware. A dev-server proxy may help local test runs, but production builds must not depend on a local-only proxy target.
- Retained mock/demo/offline modes must be explicit per profile. Production profile paths must not depend on unapproved mocks, SQLite fixtures, or local JSON data.
- Build and runtime commands must state the profile they load. Avoid commands that rely on implicit environment defaults when the artifact is handed to another workflow.

## Data Service Variables

Use the host project's naming convention, but the service profile should cover these concerns:

| Concern | Example keys |
| --- | --- |
| Runtime profile | `APP_ENV`, `NODE_ENV`, `SPRING_PROFILES_ACTIVE`, `FLASK_ENV` |
| Port/base path | `PORT`, `API_BASE_PATH`, `PUBLIC_BASE_URL` |
| Authoritative source | `DATABASE_URL`, `DATA_SOURCE_URL`, `UPSTREAM_API_BASE_URL`, `SOURCE_MODE` |
| Auth/SSO | `AUTH_BASE_URL`, `SSO_BASE_URL`, `CLIENT_ID`, `APPLICATION_KEY` |
| CORS/proxy allowlist | `CORS_ALLOWED_ORIGINS`, `GATEWAY_BASE_URL` |
| Observability | `LOG_LEVEL`, `LOG_ENV`, `TRACE_EXPORTER`, `SENTRY_DSN` |
| Health/readiness | `HEALTH_PATH`, `READINESS_PATH` |

## Data Visualization Variables

Use the frontend framework's public-env prefix when required, such as Vite `VITE_`, Next public variables, or the existing project convention.

| Concern | Example keys |
| --- | --- |
| Runtime profile | `VITE_APP_ENV`, `VITE_RUNTIME_ENV`, `NEXT_PUBLIC_APP_ENV` |
| Backend/API base | `VITE_API_BASE_URL`, `VITE_BFF_BASE_URL`, `NEXT_PUBLIC_API_BASE_URL` |
| Auth/SSO | `VITE_AUTH_BASE_URL`, `VITE_SSO_BASE_URL`, `VITE_CLIENT_ID` |
| Asset/base path | `VITE_PUBLIC_BASE`, `VITE_ASSET_BASE_URL`, `BASE_URL` |
| Provider/source mode | `VITE_PROVIDER_MODE`, `VITE_ENABLE_MOCK`, `VITE_SOURCE_MODE` |
| Observability | `VITE_LOG_ENV`, `VITE_SENTRY_DSN` |

## Verification Requirements

For every environment-sensitive handoff, record:

- Profile name: `test` or `production`.
- Config file loaded: `.env.test` or `.env.production`.
- Frontend URL and backend/API base URL for that profile.
- Auth/SSO endpoint and credential source, without leaking secrets.
- Data/source mode and whether mocks, SQLite fixtures, or demo data are retained.
- Proxy/CORS/base-path behavior.
- Build/start/preview command and evidence that it used the intended profile.
- Health/readiness endpoint or representative API check.
- Version/commit/build identifier when available.
- Blockers where the profile file, values, runtime URL, source access, auth, or health evidence is missing.

## Readiness Rules

- Mark the data-service or data-visualization handoff `ready` only when the relevant `.env.test` and `.env.production` contract is present or explicitly out of scope for a non-production deliverable.
- Mark production closed-loop readiness `partial` when `.env.production` exists but the runtime has not been smoke-tested with that profile.
- Mark production closed-loop readiness `blocked` when production-bound work has only one shared `.env`, an unknown profile, or production frontend/backend values that point to test/local/mock targets without owner approval.
