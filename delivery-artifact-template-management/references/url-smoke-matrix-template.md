# URL Smoke Matrix Template

Use this template when runtime URL readiness needs a repeatable matrix instead of ad hoc checks.

## Matrix Columns

| Case | Target | Check | Expected result | Evidence | Status |
| --- | --- | --- | --- | --- | --- |
| Frontend reachable | frontend URL | HTTP open/browser load | 200 or expected login redirect; no blank page | URL, status, screenshot/console | not run/pass/fail/blocked |
| Backend reachable | backend base/API URL | health or representative endpoint | expected status/envelope | status, response sample | not run/pass/fail/blocked |
| Version alignment | frontend/backend | build/version/branch/env | same intended environment | visible version, API doc, commit | not run/pass/fail/blocked |
| Static assets | frontend URL | CSS/JS/logo/media requests | no missing critical asset | network evidence | not run/pass/fail/blocked |
| Proxy/CORS | frontend calling backend | representative API request | no CORS/proxy failure | network evidence | not run/pass/fail/blocked |
| Production smoke | frontend/backend | health/readiness, version, auth mode, source mode, dependency and observability status | production-bound runtime signals are explicit | health/API response, version/config note, log/monitor evidence | not run/pass/fail/blocked |

## Result Rules

- Mark `blocked` when URL, account, VPN, SSO, or environment access is unavailable.
- A page that renders but points to the wrong backend is `fail`, not `pass`.
- Do not proceed to deep data/filter testing until frontend and backend readiness are both known.
- For production-bound validation, URL smoke is `partial` unless health/readiness, version alignment, auth mode, source mode, and dependency/observability status are recorded or explicitly out of scope.
