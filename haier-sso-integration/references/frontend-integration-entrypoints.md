# Haier IAM Frontend Integration Entrypoints

Use this reference to choose the correct frontend SSO entrypoint before implementing. Frontend access is not one single path: choose by project runtime, dependency style, container, router, and ownership boundary.

## Entrypoint Map

| Entrypoint | Use When | Primary Files | Required Flow |
| --- | --- | --- | --- |
| Script-tag browser SDK | Static HTML, Vue/Vite, legacy webpack, non-NPM, mixed frontend, or quick standardization by global SDK | `index.html`, `App.vue`, auth adapter, request client | Load browser SDK, wait for `window.__USERCENTER__`, configure, login, persist token, attach `Access-Token`, handle 401/403/logout. |
| Package-based IAM SDK | Project already depends on package-based `@haier/iam` or has a stable module-based auth bootstrap | package auth module, router guard, request client | Keep package workflow, wrap SDK calls in adapter, avoid adding a second script SDK, align headers/recovery/logout. |
| iHaier/Feishu container | Page runs inside iHaier/Feishu and product provides `appId` | container bootstrap, IAM adapter, request client | Configure `appId`, redirect URLs, and container permissions, then run the same login/header/recovery flow. |
| Micro-frontend, iframe, or webview | Shell/sub-app boundary, iframe storage isolation, delayed script loading, or embedded browser behavior affects login | shell entry, sub-app entry, auth adapter, routing bridge | Decide SSO owner, load SDK once where possible, handle storage/redirect boundaries, pass only safe auth context, attach headers in each protected request layer. |
| Existing SSO retrofit | SDK/login already exists but backend requests or recovery are broken | request client, route guard, auth store | Keep existing login, add missing `Access-Token`, token persistence, 401 single-flight recovery, 403 separation, and logout cleanup. |

## Shared Frontend Contract

Every entrypoint must satisfy these rules:

- Initialize IAM before protected data loading.
- Use environment-specific `ssoUrl`, `clientId`, backend `tokenUrl`, optional `redirectUri`, optional `exitUrl`, and optional `appId`.
- Test uses `https://iam-test.haier.net`; production uses `https://iama.haier.net`.
- `tokenUrl` is the business backend code-to-token service, not a browser-side call with `clientSecret`.
- The backend `tokenUrl` response must expose `resultCode`, `resultMsg`, `access_token`, `expires_in`, `token_type`, `refresh_token`, and `account` as the canonical response contract.
- Persist only browser-safe auth values, normally the access token. The configured `clientId` may remain in frontend SDK config, but it is not the authoritative token-check credential.
- Send `Access-Token: {token}` on protected backend APIs unless the backend contract explicitly defines a compatibility alias.
- Do not send `Application-Key` or `clientId` from the frontend for token check; backend code resolves the client ID from server-side configuration or a trusted tenant/app registry.
- Treat 401/token-invalid as auth recovery; treat 403 as no-permission, not as re-login.
- Clear local auth state on logout and invalid-token recovery.

## Script-Tag Browser SDK Flow

1. Inspect the app entry.
   Identify whether the app is static HTML, Vue/Vite, legacy webpack, server-rendered, or mixed. In Vue/Vite, use `index.html` for the SDK script and `App.vue` or an auth adapter for bootstrap.

2. Add the SDK script once.
   Use the approved browser build unless the project pins another approved version:

   ```html
   <script src="https://r.haier.net/assets/prod/s01996-front/haier-iam/1.9.4/browser/index.min.js"></script>
   ```

3. Wait for SDK availability.
   Read the SDK from `window.__USERCENTER__`. If the script may load after app bootstrap, use a bounded wait helper and show a recoverable error instead of leaving a blank page.

4. Build one IAM adapter.
   Centralize `waitForUserCenter`, `configUserCenter`, `login`, `logout`, `getToken`, `getUserInfo`, token persistence, and invalid-token cleanup. Components should not scatter raw SDK calls.

5. Configure the SDK.
   Call `configUserCenter` with `ssoUrl`, `clientId`, `tokenUrl`, optional `redirectUri`, optional `exitUrl`, and optional `appId`. Add `extra.locationParseEnableHash: true` for hash-router projects.

6. Start login before protected API calls.
   Call `login()` from app bootstrap or a route guard. Do not use local token existence as the primary branch. If login fails, surface `errorMessage` and stop protected data loading.

7. Persist safe auth state.
   Store the access token using stable keys or the project's existing auth store. Store the configured `clientId` only if the local frontend adapter needs it for SDK/bootstrap diagnostics; do not use it as backend token-check input. Do not store `clientSecret`, raw authorization codes, or full sensitive user payloads.

8. Attach request headers.
   Add `Access-Token` in one shared request client or interceptor. This must cover page load, route changes, refresh, and component requests.

9. Handle backend `tokenUrl` failure.
   If SDK login cannot exchange the code through `tokenUrl`, treat it as login failure. Do not let the app enter an anonymous success state.

10. Recover from 401.
   Clear stale auth, share one refresh promise across concurrent failed requests, call `login({ invalidateToken: true })`, persist the refreshed values, retry once, and stop on repeated failure.

11. Handle 403.
   Use `notPermission()` or the product no-permission state. Do not re-login for a valid-token permission failure.

12. Logout.
   Call SDK `logout()`, clear browser auth state, route cache, request cache, and local user store. Call backend logout only if the backend contract provides a local session.

## Package-Based IAM SDK Flow

Use this when the project already imports `@haier/iam` or has an established module-based IAM bootstrap. Do not add the script-tag SDK on top of an existing package integration unless the user explicitly requests migration.

1. Locate the existing auth module, package version, router guard, and request client.
2. Keep the current package import and initialize with the same required config fields: `ssoUrl`, `clientId`, and `tokenUrl`.
3. Wrap package SDK calls behind the same local adapter surface used by the app: `init`, `login`, `logout`, `getToken`, `getUserInfo`, and `refreshAfter401`.
4. Ensure startup calls `login()` before protected requests and does not depend only on stale local storage.
5. Persist only browser-safe token values; keep `clientId` in SDK config rather than treating browser storage as the backend check source.
6. Add or verify `Access-Token` request headers.
7. Implement 401 single-flight re-login and retry-once behavior.
8. Keep 403 as no-permission handling.
9. Verify refresh, deep link, route transition, invalid token, and logout.

## iHaier/Feishu Container Flow

Use this when the page runs in iHaier/Feishu or the product owner supplies a real `appId`.

1. Confirm which tenant/environment is used and whether the page is test or production.
2. Confirm Feishu/iHaier app configuration: redirect URLs, app permissions, and business page entry URLs.
3. Configure SDK with `appId` only when a real app id is supplied. Do not keep placeholders.
4. Configure `redirectUri` to the business page URL that is allowed in the container platform.
5. Run the same login, token persistence, request-header, 401, 403, and logout flow as the standard SDK path.
6. Test inside the actual container, not only in desktop Chrome, because redirect and storage behavior may differ.

## Micro-Frontend, Iframe, Or Webview Flow

Use this when the app is embedded or split across a shell and sub-apps.

1. Decide the SSO owner: shell, sub-app, or each independently deployed app.
2. Load the SDK once in the owner runtime when possible. If each sub-app owns auth, ensure each uses the same environment config and header contract.
3. Handle delayed SDK availability and storage isolation with explicit timeout and error states.
4. For iframes, avoid leaking tokens through query strings. Prefer same-origin storage or a narrowly scoped, documented bridge that passes only the required safe values.
5. Ensure each protected request client attaches `Access-Token`.
6. Coordinate route refresh and deep links so sub-app data loading waits for auth bootstrap.
7. On logout, clear shell and sub-app auth state consistently.

## Existing SSO Retrofit Flow

Use this when login already works but business APIs still show SSO breakpoints.

1. Keep the existing SDK/bootstrap unless it is clearly wrong.
2. Add missing stable storage for the access token.
3. Add missing `Access-Token` request header in the shared request client.
4. Fix 401 recovery with clear state, `login({ invalidateToken: true })`, single-flight refresh, and retry once.
5. Separate 403 permission behavior from 401 auth behavior.
6. Confirm logout clears all local state.
7. Verify clean first access, refresh, deep link, invalid token, no permission, and logout.
