# Spec: Notify Email Channel — Registration Verification & Password Reset

**Status:** ready-for-agent  
**Repos:** `home` (backend), `openapi_auth` (frontend)  
**Labels:** `ready-for-agent`

---

## Problem Statement

用户无法通过邮箱完成账号注册验证，也无法在忘记密码时通过邮箱安全地重置密码。当前系统虽在 `UserAuth` 模型中预留了 `EMAIL` 认证类型与 `ifverified` 状态字段，以及 SMTP 相关环境变量占位，但缺少：

- 邮件发送基础设施（渠道配置、发送、发送记录）
- 注册时的邮箱验证流程
- 基于邮箱的忘记密码 / 重置密码流程
- 未验证账号的登录拦截
- 密码的安全存储（当前为明文比对）

前端 `openapi_auth` 的注册仅调用旧 `signin` 端点，忘记密码为 stub，无法完成端到端认证体验。

## Solution

新增 `apps/notify` 通知模块，以 `email` 作为首个渠道（扁平结构 `apps/notify/email/`），提供 SMTP 发信、发送记录与 Redis token 管理能力。扩展 `system` 认证模块，新增注册、邮箱验证、重发验证、忘记密码、重置密码等 API；注册时同时创建 `PASSWORD`（username 登录）与 `EMAIL`（邮箱验证）两条 `UserAuth`，用户点击邮件验证链接后两条记录同时变为 `VERIFIED`，方可登录。忘记密码需同时提供用户名与注册邮箱；已激活账号收到重置链接，未激活账号自动重发验证邮件。

同步改造 `openapi_auth` 前端：注册表单、验证落地页、忘记密码与重置密码页面。

## User Stories

1. As a new user, I want to register with a username, email, and password, so that I can create an account with both login credentials and a verifiable email address.
2. As a new user, I want to receive a verification email immediately after registration, so that I can confirm I own the email address.
3. As a new user, I want to click a link in the verification email to activate my account, so that I can complete registration without entering a code.
4. As a new user, I want to see a clear page after registration telling me to check my email, so that I know what to do next.
5. As a new user, I want verification links to expire after 2 hours, so that stale links cannot be abused indefinitely.
6. As a new user, I want to request a new verification email if the link expired or I did not receive it, so that I can still activate my account.
7. As a new user, I want rate limits on resending verification emails (5-minute cooldown, max 3 per hour per email), so that the system is not abused for spam.
8. As an unverified user, I want to be blocked from logging in, so that only verified accounts can access the system.
9. As an unverified user who tries to log in, I want a clear error indicating my email is not verified, so that I know to check my email or resend verification.
10. As a verified user, I want to log in with my username and password, so that I can access the system using credentials I chose at registration.
11. As a verified user, I want my password stored securely (bcrypt hashed), so that my credentials are protected if the database is compromised.
12. As a user who forgot my password, I want to submit my username and registration email on a forgot-password form, so that the system can identify my account.
13. As a verified user who forgot my password, I want to receive a password reset link by email, so that I can set a new password securely.
14. As a verified user who forgot my password, I want reset links to expire after 30 minutes, so that leaked links have a short attack window.
15. As a verified user who forgot my password, I want to land on a reset-password page from the email link and set a new password, so that I can regain access to my account.
16. As an unverified user who submits forgot-password with matching username and email, I want the system to resend my verification email instead of a reset link, so that I am guided to activate first.
17. As an unverified user who submits forgot-password, I want an explicit message that my account is not yet activated and verification was resent, so that I understand why I did not get a reset link.
18. As a user submitting forgot-password for an activated account, I want a generic success response regardless of whether the account exists, so that attackers cannot enumerate valid accounts via this endpoint.
19. As a user registering with a taken username, I want an explicit error that the username already exists, so that I can choose a different one.
20. As a user registering with a taken email, I want an explicit error that the email is already registered, so that I can use a different email or log in.
21. As an operator, I want email channel configuration via environment variables (SMTP host, port, credentials, sender), so that I can deploy without a database config UI in the first iteration.
22. As an operator, I want every outbound email recorded with status and error details, so that I can audit and debug delivery issues.
23. As an operator, I want emails sent asynchronously after the API responds, so that slow SMTP does not block user-facing requests.
24. As an operator, I want verification and reset tokens stored in Redis with TTL, so that tokens auto-expire without manual cleanup.
25. As a developer maintaining legacy integrations, I want the existing `signin` endpoint to remain functional, so that current callers are not broken while new registration moves to `register`.
26. As a user completing OAuth flows via `openapi_auth`, I want the updated registration and login flows to coexist with GitHub OAuth, so that I can still use social login.
27. As a user clicking a verification link, I want to land on a frontend page that calls the backend to complete verification, so that I get visual confirmation of success or failure.
28. As a user clicking a reset link, I want to land on a frontend page where I enter a new password, so that the reset flow is intuitive.
29. As a user, I want verification emails to use simple HTML with a clear call-to-action button and plain-text fallback, so that emails render well across clients.
30. As a developer, I want the notify module structured so future channels (e.g. SMS) can be added alongside email, so that notification infrastructure is reusable.

## Implementation Decisions

### Module layout

- New app: `apps/notify/` registered in the top-level API router with prefix `/api/notify`.
- Email channel: flat subdirectory `apps/notify/email/` containing models, repositories, schemas, services, SMTP channel adapter, and HTML templates.
- Shared notify utilities at `apps/notify/` level: Redis client wrapper, rate-limit helpers (usable by future channels).
- Auth business orchestration remains in `apps/system` (`AuthService` extended); notify email module is responsible only for sending and recording emails, not for user identity mutations.

### Identity model at registration

- `POST /api/system/auth/register` accepts `username`, `email`, `password`.
- Creates one `User` and two `UserAuth` records in a single transaction:
  - `PASSWORD`: `identifier = username`, `credential = bcrypt(password)`, `ifverified = UNVERIFIED`
  - `EMAIL`: `identifier = email`, `credential = null`, `ifverified = UNVERIFIED`
- Uniqueness enforced by existing unique index on `(ttype, identifier)` plus explicit pre-checks for clearer error messages.
- After commit, enqueue verification email via `BackgroundTasks`.

### Email verification

- Verification method: **email link only** (no OTP).
- Token stored in Redis, TTL **2 hours**, keyed by purpose + token value; payload includes `user_id` and purpose `email_verify`.
- Link format: `{OAUTH2_LOGIN_URL}/verify-email?token={token}` (frontend landing page).
- `POST /api/system/auth/verify-email` accepts `{ token }`, validates Redis entry, sets both `PASSWORD` and `EMAIL` `UserAuth` records for that user to `VERIFIED`, deletes token.
- `POST /api/system/auth/resend-verification` accepts `{ email }`, rate-limited, resends verification email if user exists and email auth is still `UNVERIFIED`.

### Login gate

- `POST /api/system/auth/refresh_token` (login) extended: after credential match, require that the user's `EMAIL` `UserAuth` is `VERIFIED`; otherwise return a distinct error (e.g. email not verified).
- Login uses `ttype = PASSWORD`, `identifier = username`, `credential = password` (verified with bcrypt).

### Password reset

- `POST /api/system/auth/forgot-password` accepts `{ username, email }`.
- Validates username belongs to a `User` and that user's `EMAIL` auth `identifier` matches the submitted email.
- If `EMAIL` auth is `UNVERIFIED`: resend verification email, return explicit unactivated message (not generic).
- If `EMAIL` auth is `VERIFIED`: generate reset token (Redis, TTL **30 minutes**), send reset email with link `{OAUTH2_LOGIN_URL}/reset-password?token={token}`, return generic success message.
- `POST /api/system/auth/reset-password` accepts `{ token, new_password }`, validates token, bcrypt-hashes and updates `PASSWORD` credential, deletes token.
- **No** JWT / refresh_token invalidation after reset (tokens expire naturally).

### Email channel (notify)

- Configuration from environment variables, extending existing `MAIL_*` keys with `MAIL_SERVER_PORT`, `MAIL_SERVER_PASSWORD`, `MAIL_USE_TLS` (or equivalent).
- `EmailSendRecord` model (MySQL via SQLAlchemy, following `WechatMsg` pattern): fields include recipient, subject, template_type (e.g. `email_verify`, `password_reset`), body snapshot or template ref, status (`pending` / `sent` / `failed`), error message, timestamps.
- `EmailSendService`: render simple HTML template + text/plain fallback, write `pending` record, dispatch SMTP in background, update record to `sent` or `failed`.
- Rate limiting via Redis: per-email **5-minute cooldown** and **max 3 sends per hour** for verification and reset purposes.

### Password hashing

- Introduce bcrypt for `PASSWORD` credential on register and reset.
- Login path updated to `bcrypt.checkpw` instead of plaintext DB comparison.
- Legacy `signin` endpoint unchanged for backward compatibility (may still store plaintext until migrated — document as known limitation).

### API contracts (new / modified)

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/system/auth/register` | Register username + email + password |
| POST | `/api/system/auth/verify-email` | Consume verification token |
| POST | `/api/system/auth/resend-verification` | Resend verification email |
| POST | `/api/system/auth/forgot-password` | Initiate reset or resend verification |
| POST | `/api/system/auth/reset-password` | Set new password from reset token |
| POST | `/api/system/auth/refresh_token` | **Modified:** bcrypt verify + require EMAIL verified |

Response envelope: existing `SuccessResponse` / exception types.

### Frontend (`openapi_auth`)

- Register form: collect `username`, `email`, `password`; call `/register`; redirect to check-email / verify guidance view.
- New route `/verify-email`: read `token` query param, call verify API, show success/failure.
- Forgot password on login page: collect `username` + `email`, call forgot-password API.
- New route `/reset-password`: read `token` query param, form for new password, call reset-password API.
- Update `src/api/auth.js` with new endpoints; keep GitHub OAuth and existing login flow.

### Redis client

- New async Redis client module under `apps/notify/`, configured from existing `REDIS_HOST` / `REDIS_PORT` / `REDIS_DB` / `REDIS_PASSWORD` in `core/config.py`.
- Used for verification tokens, reset tokens, and send rate-limit counters.

### Database / initialization

- Register `EmailSendRecord` model; ensure table/index creation follows existing MySQL initialization patterns used by other SQLAlchemy models in the project.
- No schema change to `UserAuth` — existing fields suffice.

### Security / enumeration policy

- **Register:** explicit errors for duplicate username or email.
- **Forgot-password (activated account):** generic success response to prevent enumeration.
- **Forgot-password (unactivated account):** explicit message + auto resend verification.

### Out of scope for notify API surface

- Notify module does **not** expose public verify/reset endpoints; those stay on `system/auth` and call into notify for sending only.

## Testing Decisions

### What makes a good test

- Test **external behavior** at service boundaries: given inputs and dependency outcomes, assert API-facing results (created records, verification state, error types, whether send was scheduled).
- Do **not** test SMTP wire format, Redis key string internals, or template HTML markup.
- Mock or inject external I/O (Redis, email send service, background task scheduler).

### Primary test seam (proposed)

**Single seam: `AuthService`** — extended with injectable `UserIdentityRepository`, `NotifyEmailService` (or send interface), and `RedisTokenStore`.

Rationale: all user-visible flows (register → verify → login, forgot → reset → login, unactivated forgot → resend) are orchestrated here; notify email is a downstream dependency. One test class can cover the full decision tree without spanning API HTTP layer or real SMTP/Redis.

Example behaviors to cover at this seam:

| Scenario | Expected behavior |
|----------|-------------------|
| Register with new username + email | Two `UNVERIFIED` auths created; send verification scheduled |
| Register duplicate username | Explicit conflict error; no records created |
| Register duplicate email | Explicit conflict error |
| Verify with valid token | Both auths → `VERIFIED`; token deleted |
| Verify with expired/missing token | Error; auths unchanged |
| Login before verify | Rejected with email-not-verified error |
| Login after verify with correct password | Tokens returned |
| Forgot-password, unactivated match | Verification resend scheduled; explicit unactivated response |
| Forgot-password, activated match | Reset send scheduled; generic success response |
| Reset with valid token | Password updated (bcrypt); token deleted |
| Resend verification over rate limit | Rejected |

### Secondary seam (optional, lower priority)

- `EmailSendService` with mocked SMTP: assert record status transitions `pending → sent/failed` when send succeeds/fails.

### Prior art

- `tests/apps/repository_migration_tests.py` — `unittest.IsolatedAsyncioTestCase`, async service/repo tests.
- Service constructor injection pattern (`repo or XxxRepository(db)`) used throughout `apps/system/services/`.
- No existing FastAPI `TestClient` integration tests; avoid introducing HTTP-level tests unless seam proves insufficient.

## Out of Scope

- OTP / six-digit code verification (explicitly dropped; link-only).
- SMS or other notify channels (structure may allow later, not implemented now).
- Database-backed email channel configuration / multi-SMTP admin UI.
- JWT or refresh_token blacklist / forced logout after password reset.
- Changes to `openapi_user` console (auth UI lives in `openapi_auth`).
- Migrating legacy `signin` callers to bcrypt or email verification.
- Rich branded email templates beyond simple HTML + text fallback.
- Celery / message-queue based mail delivery.
- Internationalization of email templates.
- Admin UI for viewing send records.

## Further Notes

- `UserAuth_Ttype.EMAIL` identifier is for verification and password-recovery targeting only; login always uses `PASSWORD` + username.
- GitHub OAuth flow (`resolve_or_create_github_user`) is unaffected; may later want email verification for GitHub-created accounts — not part of this spec.
- `OAUTH2_LOGIN_URL` should point to `openapi_auth` frontend (default port 8081) for link generation, consistent with existing GitHub OAuth redirect pattern.
- Environment variables to document in deployment README: all `MAIL_*`, `REDIS_*`, and confirm `OAUTH2_LOGIN_URL`.
- Known legacy gap: existing `signin` + plaintext credentials remain for backward compatibility; new `/register` path is the secure, verified flow.
