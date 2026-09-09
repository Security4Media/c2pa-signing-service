# API Reference

This page covers behavior the OpenAPI spec doesn't capture: sync/async pairing, per-endpoint input constraints, custom assertions, parent provenance, and output placement. [openapi.json](openapi.json) is the source of truth for exact request/response schemas, field types, and status/error codes. It's generated from the private service implementation and never edited by hand here; browse it via the Swagger Editor link on the [docs homepage](../index.md). Use [cURL Examples](curl-examples.md) for runnable requests.

## Health And Jobs

### `GET /v2/health`

Liveness and readiness probe. Returns `200 OK` with an empty body.

### `GET /v2/jobs/{id}`

Retrieves the current snapshot of a batch job, async or sync: `job_id`, top-level `status`, `results`, and `timing`. `404 JOB_NOT_FOUND` if the ID doesn't exist.

## C2PA Video

`POST /v2/c2pa/video` (async) and `POST /v2/sync/c2pa/video` (sync — polls until the job reaches a terminal state or `server.sync_timeout_ms` elapses, then `408 REQUEST_TIMEOUT`).

Accepts file inputs only; a folder input returns `400 INVALID_INPUT_TYPE`. Supports [custom assertions](#custom-assertions) and [parent provenance](#parent-provenance).

## C2PA Audio

`POST /v2/c2pa/audio` (async) and `POST /v2/sync/c2pa/audio` (sync, same timeout behavior as above).

Accepts file inputs only; a folder input returns `400 INVALID_INPUT_TYPE`. Each input must be a single file whose extension names a container the C2PA SDK can sign: `mp3`, `wav`, `flac`, `m4a`, and `mp4`/`m4v` for audio-only assets. An input with no derivable extension is accepted and its media type is settled during resolution. Supports [custom assertions](#custom-assertions) and [parent provenance](#parent-provenance), with the same `params` shape as video signing.

## C2PA Fragmented

`POST /v2/c2pa/fragmented` (async) and `POST /v2/sync/c2pa/fragmented` (sync, same timeout behavior as above).

Accepts folder inputs only. `playlist_pattern`, `init_pattern`, and `frag_pattern` are required. Supports custom assertions and parent provenance, embedded into every signed init segment's manifest.

## Media Packaging

`POST /v2/package` (async) and `POST /v2/sync/package` (sync, same timeout behavior as above).

Accepts folder inputs only; no required params. Packaging-only — no signing, so custom assertions and parent provenance don't apply.

## Package And Sign

`POST /v2/c2pa/package` (async) and `POST /v2/sync/c2pa/package` (sync, same timeout behavior as above).

Accepts folder inputs only. `playlist_pattern`, `init_pattern`, and `frag_pattern` are optional. Supports custom assertions and parent provenance, same as fragmented signing.

## Custom Assertions

All four C2PA signing endpoints (`/v2/c2pa/video`, `/v2/c2pa/audio`, `/v2/c2pa/fragmented`, `/v2/c2pa/package`) accept optional custom assertions embedded in the signed manifest via `params.assertions`. Each entry is a label plus a JSON payload:

```json
"assertions": [
  {
    "label": "com.example.rights",
    "data": { "owner": "ACME Media", "license": "CC-BY-4.0" }
  }
]
```

- `label`: non-empty string; use a reverse-domain label (`com.example.*`) to avoid collisions with standard C2PA assertions.
- `data`: arbitrary JSON embedded as the assertion payload. Only JSON payloads are accepted.

For fragmented and packaged publications, the assertions are embedded into every signed init segment's manifest, so the whole publication carries the same custom assertions.

## Parent Provenance

All four C2PA signing endpoints (`/v2/c2pa/video`, `/v2/c2pa/audio`, `/v2/c2pa/fragmented`, `/v2/c2pa/package`) accept an optional parent manifest attached as a provenance ingredient via `params.parent`, with optional per-input overrides via `params.parent_overrides`. Custom assertions and parent provenance can be combined in the same request on any of these endpoints.

For fragmented and packaged publications, the supplied parent is attached to every signed init segment's manifest, marking the publication as derived from that parent. When no parent is supplied, signing still succeeds: the service treats the signed output as an edit of its own source segment by default.

A parent is either a reference token (bare ingredient, no file resolved) or a media file whose embedded C2PA manifest is read and included in the provenance chain:

```json
"parent": {
  "type": "file",
  "source": { "type": "local_file_path", "path": "./tests/fixtures/video/mp4/parent.mp4" }
}
```

```json
"parent": { "type": "reference", "reference": "urn:example:parent-asset" }
```

File sources mirror single-file inputs: `local_file_path`, or `remote_file_url` with an optional `filename_hint`.

Per-input overrides replace or disable the parent for specific inputs; `parent: null` disables it for that input:

```json
"parent_overrides": [
  {
    "input_index": 1,
    "parent": {
      "type": "file",
      "source": { "type": "remote_file_url", "url": "https://example.com/parent.mp4", "filename_hint": "parent.mp4" }
    }
  },
  { "input_index": 2, "parent": null }
]
```

## Output Selection

The `output` section chooses the destination and placement. It applies to every signing and packaging endpoint. Omitting `output` (or sending `null`) is equivalent to `{"type": "local"}` with no fields.

Two variants are selected by `type`:

- `local` — writes to the service host's filesystem under `output_sinks.local.base_dir`. Useful for local or self-hosted deployments (the files land on the machine running the service).
- `s3` — writes to object storage. This is the primary destination for hosted use. Available only when the service is built with `--features s3`, and the requested `bucket` must be present in `output_sinks.s3.buckets`.

Common fields (both variants):

- `prefix`: optional caller namespace under the sink root. `"/"` or omitted means "no request prefix".
- `name`: optional logical output folder/base for this request.

`s3` also requires `bucket`. `local` takes no extra fields. The file-leaf naming
convention is **not** a request field; it is configured per output sink in the
service config (`output_sinks.*.naming`, see [Request Output Types](../guides/configuration.md#request-output-types)).

### Naming and paths

Each input contributes its own leaf name, derived from the input reference. The
per-sink `naming` setting (`derived` default | `in_place`) controls single-file
outputs:

- Single-file (video, audio) inputs: `derived` produces `{stem}_c2pa.{ext}` (e.g. `clip.mp4` → `clip_c2pa.mp4`); `in_place` keeps the input filename (`clip.mp4`).
- Folder / publication inputs (fragmented, package, package-and-sign): the leaf is the input folder's name; the `naming` setting does not apply.

The final location is composed as:

```
<base_prefix (config)> / <output.prefix> / <output.name> / <per-input-leaf>
```

For `local`, `base_prefix` is `output_sinks.local.base_dir`; for `s3` it is `output_sinks.s3.base_prefix` (may be empty). There is no job or batch id segment in the path. Reusing the same destination overwrites it — callers own uniqueness (differentiate via `prefix` or `name`).

## Feature-Gated Behavior

### `openapi`

- Exposes the runtime machine-readable spec at `/openapi.json`
- Enables generation of the runtime and synchronized docs-site raw spec

### `scalar-docs`

- Extends `openapi`
- Exposes the Scalar UI at `/docs`

### `s3`

- Enables S3-backed remote inputs
- Enables request-selected S3 output destinations
- The docs build uses the full documentation profile and generates the raw spec with `openapi` and `s3` enabled

## Watermark Placeholders

### `POST /v2/watermark`

- Purpose: reserved placeholder for future softbinding watermark creation
- Current behavior: `501 Not Implemented`
- Body: plain text `Coming soon`

### `GET /v2/watermark/{id}`

- Purpose: reserved placeholder for future softbinding watermark retrieval
- Current behavior: `501 Not Implemented`
- Body: plain text `Coming soon`

## Error Model

Errors share one shape (`ApiErrorResponse`: `error.code`, `error.message`, optional `error.details`). The OpenAPI spec lists every error code per endpoint with example payloads. `JOB_NOT_FOUND` and `REQUEST_TIMEOUT` map directly to the job-polling behavior described above.

## Operational Notes

- All processing endpoints accept batched requests via `inputs`, but the array must contain at least one input.
- Sync endpoints poll until the job reaches a terminal state or `server.sync_timeout_ms` is exceeded.
- Partial job completion is surfaced as `status: "failed"` in the HTTP response model.
- Request body size is capped by `server.max_upload_bytes`.
