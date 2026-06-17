# SSO Case Matrix Template

Use this template when SSO behavior needs repeatable runtime evidence.

## Minimum Cases

| Case | Precondition | Action | Expected frontend behavior | Expected backend/auth behavior | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| First access | no local token | open protected page | redirects/logs in through SSO | protected APIs wait for valid token | storage, network, screenshot | not run/pass/fail/blocked |
| Valid token | token present | refresh or route jump | page loads without login loop | auth headers accepted | headers/status | not run/pass/fail/blocked |
| Missing token | token cleared | call protected route/API | re-login or auth state shown | 401/normalized unauth | storage/status | not run/pass/fail/blocked |
| Invalid token | tampered/expired token | refresh/call API | clears stale state and re-login | backend rejects invalid token | status/network | not run/pass/fail/blocked |
| No permission | valid token, insufficient role | open restricted feature | no-permission state | 403/permission error | screenshot/status | not run/pass/fail/blocked |
| Logout | logged in | click logout | local auth cleared and redirected | session/token policy followed | storage/network | not run/pass/fail/blocked |

## Evidence Rules

- Capture storage keys, request header names, status codes, and user-facing state.
- Never paste real tokens, secrets, or account payloads into the final report.
