# Haier IAMA Backend Integration Entrypoints

Use this reference to choose the correct backend SSO entrypoint before implementing. Backend access is not one single path: projects may use the official Java SDK, direct IAMA API calls, a local session/JWT bridge, or a gateway/middleware-only retrofit.

## Entrypoint Map

| Entrypoint | Use When | Primary Modules | Required Flow |
| --- | --- | --- | --- |
| Java SDK integration | Spring Boot/Spring backend can use `iam-auth-sdk-starter`; official SDK dependency is acceptable | controller, SDK config, auth service, middleware | Configure SDK, expose `tokenUrl`, exchange code with SDK, map user, protect APIs, return 401/403 correctly. |
| Direct backend API integration | Non-Java backend, SDK unavailable, or team wants explicit HTTP calls | IAMA client/gateway, token controller, auth middleware | Call `/api/oauth/code/get/v2`, call `/api/oauth/token/check`, normalize errors, protect APIs. |
| Local session/JWT bridge | Existing app already has local session/JWT/permission model | token service, user mapper, session/JWT issuer, middleware | Exchange IAMA token, map account to local user, issue local context, still document whether IAMA token check remains required. |
| Gateway or middleware retrofit | Login works but protected API validation is missing or inconsistent | middleware/filter/interceptor, public allowlist, request context | Read `Access-Token`, resolve server-side client ID, call token check, attach user context, enforce 401/403 boundary. |
| Multi-client or tenant-aware backend | More than one frontend client ID or tenant can call the backend | client registry, secret resolver, auth gateway | Resolve configured credentials from trusted tenant/app context, avoid arbitrary browser-driven credential selection. |

## Shared Backend Contract

Every entrypoint must satisfy these rules:

- `clientSecret` is server-side only.
- The frontend `tokenUrl` points to a business backend endpoint, not directly to IAMA with browser credentials.
- Frontend-facing login/tokenUrl responses preserve the canonical fields `resultCode`, `resultMsg`, `access_token`, `expires_in`, `token_type`, `refresh_token`, and `account`.
- Protected browser requests carry `Access-Token: {token}`. They do not need to carry `Application-Key` for token check.
- Backend obtains `clientId` from server-side configuration or a trusted tenant/app registry before calling IAMA. It must not trust browser-provided `clientId` or `Application-Key` as the check credential source.
- Backend calls IAMA token check with server-resolved `clientId` as both `client_id` and upstream `Application-Key`, plus the frontend-provided `Access-Token`.
- Token is valid only when `resultCode == "0"` and `data == true`.
- Missing, expired, invalid, malformed, or unverifiable auth returns 401 or the service's normalized token-invalid response.
- 403 is reserved for valid-token users who lack business permission.
- Public routes and health checks must be explicitly allowlisted.

## Java SDK Integration Flow

Use this when the backend is Spring Boot 2.0+ or compatible Spring and can use the official SDK dependency.

1. Add the SDK dependency.

   ```xml
   <dependency>
     <groupId>com.haier</groupId>
     <artifactId>iam-auth-sdk-starter</artifactId>
     <version>1.1.7</version>
   </dependency>
   ```

2. Configure SDK properties.

   ```yaml
   iam:
     auth:
       sdk:
         config:
           authHost: https://iam-test.haier.net/api
           clientId: your-client-id
           clientSecret: your-client-secret
   ```

3. Expose the frontend `tokenUrl`.
   Provide a backend endpoint such as `/getTokenAndUserInfo` or the project's standard auth route. It accepts `code` from the frontend SDK and never accepts `clientSecret` from the browser.

4. Exchange code through the SDK.
   Call the SDK service method to exchange authorization code for token and user info. Treat non-success SDK responses as auth failures.

5. Preserve and normalize response fields.
   Preserve canonical token fields as the frontend-facing response: `resultCode`, `resultMsg`, `access_token`, `expires_in`, `token_type`, `refresh_token`, and `account`. Do not make top-level `token`/`userInfo` aliases the only contract.

6. Map account to local user.
   Bind IAMA account fields to local user, role, org, and permission context.

7. Protect business APIs.
   Add middleware/filter/interceptor so protected routes read `Access-Token`, resolve `clientId` from backend configuration, and verify token validity. If the SDK does not cover request-time token validation, call the IAMA token-check API through a small gateway.

8. Return correct status.
   Return 401/token-invalid for invalid auth and 403 for valid-token permission denial.

9. Test SDK and middleware boundaries.
   Cover successful code exchange, failed exchange, missing code, missing headers, invalid token, no permission, and public allowlist behavior.

## Direct Backend API Integration Flow

Use this for Python, Node, Go, .NET, custom Java, or any backend where the Java SDK is unavailable or not desired.

1. Create one IAMA HTTP gateway.
   Encapsulate remote base URL, timeouts, retry policy, client ID, client secret, and response normalization.

2. Implement code exchange.
   Call:

   ```http
   POST {baseUrl}/api/oauth/code/get/v2
   Content-Type: application/json
   ```

   Request body:

   ```json
   {
     "client_id": "your-client-id",
     "client_secret": "server-side-secret",
     "code": "frontend-code"
   }
   ```

3. Validate exchange success.
   Treat success as `resultCode == "0"` plus present `data.access_token`. Fail closed on missing token, malformed response, timeout, or upstream error.

4. Implement token check.
   Call:

   ```http
   GET {baseUrl}/api/oauth/token/check?client_id={serverConfiguredClientId}
   Application-Key: {serverConfiguredClientId}
   Access-Token: {accessToken}
   ```

5. Validate token check success.
   Treat valid as `resultCode == "0" && data == true`. Any other response is unauthenticated.

6. Protect routes through middleware.
   Read `Access-Token` from every protected request, resolve the allowed client ID from backend config or trusted tenant/app context, call token check, attach user context, and continue to business logic only after success.

7. Normalize errors.
   Convert upstream failures to the service's unauthenticated/upstream-auth-failed error types. Redact tokens, codes, secrets, and full account payloads from logs and responses.

8. Test failure modes.
   Include missing `Access-Token`, missing backend client ID config, invalid token, upstream timeout, malformed response, and route allowlist mistakes.

## Local Session Or JWT Bridge Flow

Use this when the backend already has local login, sessions, JWTs, or a mature permission model.

1. Exchange the frontend code through SDK or direct API.
2. Map IAMA account to local user by stable identifiers such as account id, `userName`, `account`, `domain`, or `tenantId`.
3. Load local roles, organizations, data scopes, and feature permissions.
4. Issue the existing local session or JWT if the product contract requires it.
5. Document whether later browser requests still include IAMA `Access-Token`; `Application-Key` remains backend-resolved for token check unless a legacy compatibility exception is explicitly approved.
6. If local session replaces repeated IAMA token checks, document the explicit product/security decision and expiry policy.
7. Keep 401/403 behavior aligned: invalid session or invalid token is 401; valid identity without permission is 403.
8. Align logout so SDK logout and local session invalidation do not leave stale state.

## Gateway Or Middleware Retrofit Flow

Use this when code exchange already works but protected business APIs are weak, inconsistent, or missing auth checks.

1. Inventory protected and public routes.
2. Add a small public allowlist for health checks, static assets, login/tokenUrl, and preflight when needed.
3. For every other business API, require `Access-Token`.
4. Resolve `clientId` from backend configuration or trusted tenant/app context.
5. Call IAMA `token/check` with backend-resolved `Application-Key` and the request `Access-Token`.
6. Attach local user context only after token validity is confirmed.
7. Return 401/token-invalid for auth failure.
8. Return 403 only after local permission checks fail for a valid token.
9. Add tests proving business routes cannot bypass the middleware.

## Multi-Client Or Tenant-Aware Flow

Use this when multiple frontend client IDs or tenants call the same backend.

1. Build an explicit client registry with allowed server-side client IDs.
2. Resolve client IDs and client secrets only from server-side configuration, tenant registration, origin/app mapping, or secret storage.
3. Reject requests whose trusted tenant/app context cannot resolve a configured client ID before upstream calls.
4. Never let arbitrary browser-provided client IDs or `Application-Key` headers select credentials dynamically.
5. Bind client ID to tenant, redirect/origin allowlist, and permission scope when needed.
6. Test known tenant/app, unresolved tenant/app, mismatched token/client ID, and disabled client scenarios.
