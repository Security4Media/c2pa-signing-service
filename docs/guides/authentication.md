# Authentication And Authorization

A build of the service with the `oidc` feature accepts a request only with a valid OAuth 2.0 access token from the
deployment's OpenID Connect provider, and checks what that token allows. A build without the feature accepts every
request and logs a warning at startup saying so. Whether a given deployment enforces authentication depends on how it
was built; ask its operator.

The exact per-operation requirements are also in [openapi.json](../api/openapi.json): the `bearer` security scheme,
the scope each operation lists, and its `401` and `403` responses.

## What Needs A Token

| Route | Needs |
|---|---|
| `GET /v2/health`, `GET /v2/ready` | Nothing. Probes carry no token. |
| `/metrics`; `/openapi.json` and `/docs` in builds that serve them | Nothing, in every build. See [For Operators](#for-operators). |
| `POST /v2/c2pa/video`, `/v2/c2pa/audio`, `/v2/c2pa/fragmented`, `/v2/c2pa/package` and their `/v2/sync/...` variants | A token with `c2pa:sign`. |
| `POST /v2/package`, `POST /v2/sync/package` | A token with `c2pa:package`. |
| `GET /v2/jobs/{id}` | A token; see [Job Visibility](#job-visibility). |
| Every other `/v2` route (for example the watermark placeholders) | A token. |

Package-and-sign (`/v2/c2pa/package`) signs, so it needs `c2pa:sign`, not `c2pa:package`.

## Getting A Token

Callers are machine clients. Each one is registered with the identity provider as a confidential client and gets its
tokens with the OAuth 2.0 client credentials grant. The scopes are assigned to the client by the provider's
administrator; with the recommended setup they are in every token the client gets, so the request names none.

```bash
TOKEN=$(curl -s -u "${CLIENT_ID}:${CLIENT_SECRET}" \
  -d grant_type=client_credentials \
  "${ISSUER}/protocol/openid-connect/token" | jq -r .access_token)
```

`ISSUER` is the provider's issuer URL, for example `https://keycloak.example.org/realms/example`. The token endpoint path
above is Keycloak's; other providers publish theirs as `token_endpoint` in `${ISSUER}/.well-known/openid-configuration`.

Send the token on every request:

```bash
curl -H "Authorization: Bearer ${TOKEN}" https://c2pa.example.org/v2/jobs/${JOB_ID}
```

Tokens are short-lived (Keycloak's default is 5 minutes). Get a new one when it expires; the service allows 30 seconds
of clock skew by default. Send exactly one `Authorization` header.

## Scopes

| Scope | Allows |
|---|---|
| `c2pa:sign` | Submitting C2PA signing jobs, including package-and-sign. |
| `c2pa:package` | Submitting packaging-only jobs. |
| `c2pa:jobs:read:all` | Reading any client's job, not only your own. Meant for operators and support tools. |

Scope names are prefixed with `c2pa:` so they cannot clash with another service's scopes in the same identity
provider. What keeps a token issued for another service out is the audience check: the token's `aud` must name this
service.

## Job Visibility

- A client can always read the jobs it submitted. No scope is needed for that.
- Another client's job answers `404 JOB_NOT_FOUND`, exactly like an id that does not exist, so job ids cannot be
  probed.
- `c2pa:jobs:read:all` reads any job, including jobs submitted before authentication was enabled, which have no
  recorded submitter.
- Sync endpoints return the result in the response, so they need no read access at all.

Authorization is decided once, when a job is accepted. A job that was accepted keeps running even if the client's
scope is removed afterwards; short token lifetimes bound how long a removed client can keep submitting.

## Errors

| Status | Body `error.code` | `WWW-Authenticate` | When |
|---|---|---|---|
| `401` | `UNAUTHORIZED` | `Bearer` | No token was sent. |
| `401` | `UNAUTHORIZED` | `Bearer error="invalid_token"` | The token was refused: expired, bad signature, wrong issuer or audience, not an access token (for example an ID token), or the provider's signing keys are unavailable. Also an `Authorization` header that is not exactly one `Bearer <token>` (another scheme, two headers, two tokens). |
| `403` | `FORBIDDEN` | `Bearer error="insufficient_scope", scope="c2pa:sign"` | The token is valid but lacks the scope the operation needs. The header and the message name that scope. |
| `404` | `JOB_NOT_FOUND` | none | The job does not exist, or belongs to another client. |

The `401` message is the same for every cause. Why a token was refused is recorded in the service's log for the
operator, not returned to the caller.

The scope check comes after the body is read as the endpoint's JSON and before its content is validated, so a client
without the scope gets `403` rather than a `400` validation error. A body that cannot be read at all is answered
before the scope check, with a plain-text error rather than the JSON error body: `415` without
`Content-Type: application/json`, `400` for malformed JSON, `422` for JSON that does not fit the endpoint (a missing
field, a wrong type, an unknown input `type`), and `413` for a body over the configured size limit.

## Trying It In The API Docs

In a build with `scalar-docs`, open `/docs`, choose the `bearer` authentication, and paste an access token. The page
sends it with each test request and does not store it.

## For Operators

Build with `--features oidc` and add an `[auth.oidc]` section; see [Configuration](configuration.md#authoidc). Startup
connects to the provider before the server accepts requests and fails if it cannot. A build with the feature refuses
to start without the section, and a build without it refuses the section, so a configuration that asks for
authentication never runs without it. A build without `oidc` and without the section runs open to anyone who can reach
it, and says so in a `warn` line (`signal = degraded`) at startup.

`/metrics`, and `/openapi.json` and `/docs` where they are served, need no token in any build. `/metrics` reports queue
depth and ages and is meant to be scraped from inside the network; keep these routes off public ingress.

The identity provider must:

- publish an OpenID Connect discovery document at `{issuer}/.well-known/openid-configuration`, with a `jwks_uri` for
  its signing keys;
- issue access tokens as JWTs signed with an asymmetric algorithm (`RS256` by default), with a key id (`kid`) in the
  header that names a key in that set;
- put `exp`, `iat` and a payload `typ` equal to the configured `token_type` (`Bearer` by default, as Keycloak writes
  it) into every access token. Providers that mark access tokens only with the RFC 9068 header `typ: at+jwt` and no
  payload `typ` are not supported yet;
- put the configured `audience` into the token's `aud` claim. In Keycloak, give every calling client a default client
  scope with an audience mapper for this service;
- put the permissions into the standard `scope` claim, and the client id into `azp` or `client_id`;
- keep its issuer URL fixed. In Keycloak, set the hostname (`KC_HOSTNAME`), or the issuer follows the host each
  request used and tokens fail the issuer check.

Recommended Keycloak setup: a current 26.x release; one confidential client per caller with only the service account
(client credentials) flow enabled; the `c2pa:` scopes as default client scopes of the clients that need them; and none
of Keycloak's `profile`, `email`, `roles`, `web-origins` or `acr` scopes on those clients, which add claims this
service does not use.

Every log line of an authenticated request, from `request received` to `request completed`, carries the caller's
`client_id`, and the `batch submitted` line joins it to the `job_id` that the job's later lines carry. Tokens are never
logged.

For development, the service's implementation repository ships a local Keycloak with a ready realm. Its credentials
are fixed and public, so never use that realm anywhere else.

## Not Built Yet

- Tenants: grouping callers and jobs by organization, with rules such as "same tenant only".
- Per-client limits on which signers or output locations a client may use.
- Revoking jobs that are already queued when a client's access is removed.
- Human sign-in: people are expected to use a separate web front end that calls this API with tokens; the API itself
  stays bearer-token only.
