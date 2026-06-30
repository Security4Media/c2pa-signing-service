# API v2 Quick Reference

Use this page as the short-form summary. For the canonical route-by-route contract, see [API Reference](reference.md).

## Build And Run

```bash
cargo build -p service-http
cargo run -p service-http
```

Optional feature builds:

```bash
# Enable OpenAPI JSON at /openapi.json
cargo run -p service-http --features openapi

# Enable OpenAPI JSON and Scalar UI at /docs
cargo run -p service-http --features "openapi scalar-docs"

# Enable S3-backed inputs and request-selectable S3 outputs
cargo run -p service-http --features s3
```

## Runtime Configuration

The service loads `config/service.toml` by default.

```bash
RUST_LOG=info
SERVICE_CONFIG_PATH=config/service.toml
SERVICE__SERVER__BIND_ADDR=127.0.0.1:8080
SERVICE__SERVER__SYNC_TIMEOUT_MS=120000
SERVICE__SERVER__SYNC_POLL_INTERVAL_MS=250
SERVICE__SERVER__MAX_UPLOAD_BYTES=52428800
```

## Endpoint Overview

| Purpose | Async Endpoint | Sync Endpoint | Accepted Inputs |
|---------|----------------|---------------|-----------------|
| Sign monolithic video assets | `POST /v2/c2pa/video` | `POST /v2/sync/c2pa/video` | file inputs |
| Sign fragmented/HLS publications | `POST /v2/c2pa/fragmented` | `POST /v2/sync/c2pa/fragmented` | folder inputs |
| Package media publications | `POST /v2/package` | `POST /v2/sync/package` | folder inputs |
| Package and sign | `POST /v2/c2pa/package` | `POST /v2/sync/c2pa/package` | folder inputs |
| Poll async job state | `GET /v2/jobs/{id}` | - | - |
| Health probe | `GET /v2/health` | - | - |
| Softbinding placeholder | `POST /v2/watermark` | - | not implemented |
| Softbinding placeholder | `GET /v2/watermark/{id}` | - | not implemented |

## Input Types

Current request inputs are provider-agnostic:

```json
{"type": "in_request", "media_type": "video/mp4", "data_base64": "AA==", "filename": "clip.mp4"}
{"type": "local_file_path", "path": "./tests/fixtures/video/mp4/video1.mp4"}
{"type": "local_folder_path", "path": "./tests/fixtures/hls/publication"}
{"type": "remote_file_url", "url": "https://example.com/video.mp4", "filename_hint": "video.mp4"}
{"type": "remote_folder_url", "url": "s3://media-bucket/publication/"}
```

Processor rules:

- `c2pa/video` accepts file inputs only.
- `c2pa/fragmented`, `package`, and `c2pa/package` accept folder inputs only.

## Output Selection

If `output` is omitted or `null`, artifacts are written under the configured local sink rooted at `output_sinks.local.base_dir`.

With the `s3` feature enabled and `[output_sinks.s3]` configured, requests may select an S3 destination:

```json
{
  "output": {
    "type": "s3",
    "bucket": "processed-media",
    "prefix": "exports/c2pa"
  }
}
```

Notes:

- There is no request `local_path` output type.
- Only buckets listed in `output_sinks.s3.buckets` are accepted.
- `prefix: "/"` writes at the configured `base_prefix` root when one is set.

## Request Shape

```json
{
  "inputs": [
    {
      "type": "remote_file_url",
      "url": "https://example.com/video.mp4",
      "filename_hint": "video.mp4"
    }
  ],
  "params": {},
  "output": null,
  "options": {
    "max_files_parallel": 2
  }
}
```

## Processor Parameters

### C2PA Video

```json
{
  "params": {
    "output_name": "signed-video.mp4",
    "options": {
      "timeout_ms": 2500,
      "in_place": false
    },
    "assertions": [
      { "label": "com.example.rights", "data": { "owner": "ACME Media" } }
    ],
    "parent": {
      "type": "file",
      "source": { "type": "local_file_path", "path": "./parent.mp4" }
    }
  }
}
```

`assertions`, `parent`, and `parent_overrides` are accepted by all three C2PA endpoints (`/v2/c2pa/video`, `/v2/c2pa/fragmented`, `/v2/c2pa/package`) and can be combined in one request. They do not apply to the packaging-only `/v2/package` endpoint. See [Custom Assertions](reference.md#custom-assertions) and [Parent Provenance](reference.md#parent-provenance).

### C2PA Fragmented

```json
{
  "params": {
    "publication_name": "demo-publication",
    "playlist_pattern": "**/*.m3u8",
    "init_pattern": "**/init*.mp4",
    "frag_pattern": "seg*.m4s",
    "assertions": [
      { "label": "com.example.rights", "data": { "owner": "ACME Media" } }
    ],
    "parent": {
      "type": "file",
      "source": { "type": "local_file_path", "path": "./parent.mp4" }
    }
  }
}
```

### Package

```json
{
  "params": {
    "output_name": "publication"
  }
}
```

### Package And Sign

```json
{
  "params": {
    "output_name": "publication",
    "playlist_pattern": "**/*.m3u8",
    "init_pattern": "**/init*.mp4",
    "frag_pattern": "seg*.m4s",
    "assertions": [
      { "label": "com.example.rights", "data": { "owner": "ACME Media" } }
    ],
    "parent": { "type": "reference", "reference": "urn:example:parent-asset" }
  }
}
```

## Response Shapes

### Async Submission

```json
{
  "job_id": "01234567-89ab-cdef-0123-456789abcdef",
  "status": "queued"
}
```

### Sync Completion Or Job Polling

```json
{
  "job_id": "01234567-89ab-cdef-0123-456789abcdef",
  "status": "succeeded",
  "results": [
    {
      "input_index": 0,
      "status": "succeeded",
      "output_path": "./.artifacts/output/batch-1/signed-video.mp4"
    }
  ],
  "timing": {
    "queued_at": "2026-04-09T08:00:00Z",
    "started_at": "2026-04-09T08:00:01Z",
    "finished_at": "2026-04-09T08:00:05Z"
  }
}
```

### Health

`GET /v2/health` returns HTTP `200 OK` with an empty body.

### Softbinding Placeholders

`POST /v2/watermark` and `GET /v2/watermark/{id}` currently return HTTP `501 Not Implemented` with body `Coming soon`.

## Errors

| Code | HTTP Status | Meaning |
|------|-------------|---------|
| `INVALID_INPUT_TYPE` | 400 | Processor received the wrong input category |
| `VALIDATION_FAILED` | 400 | Request or output selection failed validation |
| `JOB_NOT_FOUND` | 404 | No job exists for the requested ID |
| `REQUEST_TIMEOUT` | 408 | Sync endpoint timed out while polling |
| `PROCESSING_FAILED` | 500 | The worker failed while resolving, processing, or writing outputs |
| `INTERNAL_ERROR` | 500 | Unexpected server-side failure |

## Operational Notes

- All processing endpoints accept batched requests via `inputs`, but the array must contain at least one input.
- Sync endpoints poll until the job reaches a terminal state or `server.sync_timeout_ms` is exceeded.
- Partial job completion is surfaced as `status: "failed"` in the HTTP response model.
- Request body size is capped by `server.max_upload_bytes`.

## See Also

- [API Reference](reference.md)
- [cURL Examples](curl-examples.md)
- [Configuration Guide](../guides/configuration.md)
- [Getting Started](../guides/getting-started.md)
