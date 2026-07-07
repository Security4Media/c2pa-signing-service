# API Reference

This page is the canonical human-written contract for the current `service-http` v2 API. Use it for behavior, wire shape, and feature-gated capability notes. Use [API cURL Examples](curl-examples.md) for runnable requests and [openapi.json](openapi.json) for the generated machine-readable specification synchronized from the private service implementation.

## Health And Jobs

### `GET /v2/health`

- Purpose: liveness and readiness probe for the HTTP service
- Success: `200 OK`
- Body: empty

### `GET /v2/jobs/{id}`

- Purpose: retrieve the current snapshot of an asynchronous or synchronous batch job
- Success: `200 OK` with `job_id`, top-level `status`, `results`, and `timing`
- Errors:
  - `404 JOB_NOT_FOUND` when the batch ID does not exist
  - `500 PROCESSING_FAILED` or `500 INTERNAL_ERROR` for unexpected service-side failures

## C2PA Video

### `POST /v2/c2pa/video`

- Purpose: submit monolithic video signing as an asynchronous job
- Accepted inputs: file inputs only
  - `in_request`
  - `local_file_path`
  - `remote_file_url`
- Request fields:
  - `inputs`: required, one or more file inputs
  - `params.options.timeout_ms`: optional
  - `params.assertions`: optional custom assertions (see [Custom Assertions](#custom-assertions))
  - `params.parent`: optional parent provenance (see [Parent Provenance](#parent-provenance))
  - `params.parent_overrides`: optional per-input parent overrides
  - `output`: optional destination and placement (see [Output Selection](#output-selection)); omitted means the configured local sink
  - `options.max_files_parallel`: optional
- Success: `200 OK` with `job_id` and `status = "queued"`
- Errors:
  - `400 INVALID_INPUT_TYPE` for folder-style inputs
  - `400 VALIDATION_FAILED` for malformed or disallowed payloads
  - `500 PROCESSING_FAILED` or `500 INTERNAL_ERROR`

### `POST /v2/sync/c2pa/video`

- Purpose: submit monolithic video signing and poll until completion
- Accepted inputs: same as async endpoint
- Success: `200 OK` with final `JobResultResponse`
- Timeout: `408 REQUEST_TIMEOUT` when the job does not finish within `server.sync_timeout_ms`
- Errors: same validation and server-side failure model as the async endpoint

## C2PA Fragmented

### `POST /v2/c2pa/fragmented`

- Purpose: submit fragmented/HLS signing as an asynchronous job
- Accepted inputs: folder inputs only
  - `local_folder_path`
  - `remote_folder_url`
- Required params:
  - `playlist_pattern`
  - `init_pattern`
  - `frag_pattern`
- Optional params:
  - `assertions`: custom assertions (see [Custom Assertions](#custom-assertions))
  - `parent`: parent provenance (see [Parent Provenance](#parent-provenance))
  - `parent_overrides`: per-input parent overrides
- Optional fields:
  - `output`: optional destination and placement (see [Output Selection](#output-selection))
- Success: `200 OK` with queued job response
- Errors:
  - `400 INVALID_INPUT_TYPE` for file inputs
  - `400 VALIDATION_FAILED`
  - `500 PROCESSING_FAILED` or `500 INTERNAL_ERROR`

### `POST /v2/sync/c2pa/fragmented`

- Purpose: submit fragmented/HLS signing and wait for completion
- Accepted inputs: same as async endpoint
- Success: `200 OK` with final `JobResultResponse`
- Timeout: `408 REQUEST_TIMEOUT`
- Errors: same validation and server-side failure model as the async endpoint

## Media Packaging

### `POST /v2/package`

- Purpose: submit packaging-only processing as an asynchronous job
- Accepted inputs: folder inputs only
  - `local_folder_path`
  - `remote_folder_url`
- Params: none required (`params` may be omitted or `{}`)
- Optional fields:
  - `output`: optional destination and placement (see [Output Selection](#output-selection))
- Success: `200 OK` with queued job response
- Errors:
  - `400 INVALID_INPUT_TYPE`
  - `400 VALIDATION_FAILED`
  - `500 PROCESSING_FAILED` or `500 INTERNAL_ERROR`

### `POST /v2/sync/package`

- Purpose: package media and wait for terminal job state
- Accepted inputs: same as async endpoint
- Success: `200 OK` with final `JobResultResponse`
- Timeout: `408 REQUEST_TIMEOUT`
- Errors: same validation and server-side failure model as the async endpoint

## Package And Sign

### `POST /v2/c2pa/package`

- Purpose: package media and apply C2PA signing in one asynchronous job
- Accepted inputs: folder inputs only
  - `local_folder_path`
  - `remote_folder_url`
- Optional params:
  - `playlist_pattern`
  - `init_pattern`
  - `frag_pattern`
  - `assertions`: custom assertions (see [Custom Assertions](#custom-assertions))
  - `parent`: parent provenance (see [Parent Provenance](#parent-provenance))
  - `parent_overrides`: per-input parent overrides
- Optional fields:
  - `output`: optional destination and placement (see [Output Selection](#output-selection))
- Success: `200 OK` with queued job response
- Errors:
  - `400 INVALID_INPUT_TYPE`
  - `400 VALIDATION_FAILED`
  - `500 PROCESSING_FAILED` or `500 INTERNAL_ERROR`

### `POST /v2/sync/c2pa/package`

- Purpose: package and sign while waiting for completion
- Accepted inputs: same as async endpoint
- Success: `200 OK` with final `JobResultResponse`
- Timeout: `408 REQUEST_TIMEOUT`
- Errors: same validation and server-side failure model as the async endpoint

## Custom Assertions

All three C2PA signing endpoints (`/v2/c2pa/video`, `/v2/c2pa/fragmented`, `/v2/c2pa/package`) accept optional custom assertions embedded in the signed manifest via `params.assertions`. Each entry is a label plus a JSON payload:

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

All three C2PA signing endpoints (`/v2/c2pa/video`, `/v2/c2pa/fragmented`, `/v2/c2pa/package`) accept an optional parent manifest attached as a provenance ingredient via `params.parent`, with optional per-input overrides via `params.parent_overrides`. Custom assertions and parent provenance can be combined in the same request on any of these endpoints.

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

- Single-file (video) inputs: `derived` produces `{stem}_c2pa.{ext}` (e.g. `clip.mp4` → `clip_c2pa.mp4`); `in_place` keeps the input filename (`clip.mp4`).
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

| Code | HTTP Status | Meaning |
|------|-------------|---------|
| `INVALID_INPUT_TYPE` | 400 | Processor received a mismatched input category |
| `VALIDATION_FAILED` | 400 | Request fields or selected output failed validation |
| `JOB_NOT_FOUND` | 404 | The requested batch ID does not exist |
| `REQUEST_TIMEOUT` | 408 | Sync polling exceeded `server.sync_timeout_ms` |
| `PROCESSING_FAILED` | 500 | Job execution failed while resolving, processing, or writing outputs |
| `INTERNAL_ERROR` | 500 | Unexpected internal service failure |
