# Getting Started

## Prerequisites

- Linux or macOS
- Rust toolchain with edition 2024 support
- FFmpeg available on `PATH`
- Bento4 tools available on `PATH`, especially `mp4fragment` and `mp4dash`

Verify the external tools:

```bash
ffmpeg -version
mp4fragment
mp4dash
```

## Build The Workspace

```bash
cargo build --workspace
```

Optional validation before first run:

```bash
cargo test --workspace --no-run
```

## Configure The Service

The HTTP service loads `config/service.toml` by default. The checked-in default enables:

- bind on `0.0.0.0:8080`
- local output sink at `./.artifacts/output`
- C2PA settings from `config/c2pa/default_c2pa_sdk_settings.toml`
- media packager pipeline from `config/media-packager/media_packager_pipeline.toml`

Useful overrides:

```bash
export RUST_LOG=info
export SERVICE_CONFIG_PATH=config/service.toml
export SERVICE__SERVER__BIND_ADDR=127.0.0.1:8080
export SERVICE__SERVER__SYNC_TIMEOUT_MS=120000
```

See the [Configuration Guide](configuration.md) for the full runtime model, including S3 and feature-gated behavior.

## Start The Service

```bash
cargo run -p service-http
```

To expose generated API docs:

```bash
cargo run -p service-http --features openapi
cargo run -p service-http --features "openapi scalar-docs"
```

To preview the docs site itself:

```bash
make docs-serve
```

## First Requests

### Health Probe

```bash
curl -i http://localhost:8080/v2/health
```

Expected result: HTTP `200 OK` with an empty body.

### Sign A Video Synchronously

```bash
curl -X POST http://localhost:8080/v2/sync/c2pa/video \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [
      {
        "type": "local_file_path",
        "path": "./tests/fixtures/video/mp4/video1.mp4"
      }
    ],
    "params": {
      "output_name": "signed-video.mp4"
    }
  }'
```

Example response:

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

### Submit An Async Job And Poll It

```bash
curl -X POST http://localhost:8080/v2/c2pa/video \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [
      {
        "type": "remote_file_url",
        "url": "https://example.com/video.mp4",
        "filename_hint": "video.mp4"
      }
    ],
    "params": {}
  }'
```

Response:

```json
{
  "job_id": "01234567-89ab-cdef-0123-456789abcdef",
  "status": "queued"
}
```

Poll the job:

```bash
curl http://localhost:8080/v2/jobs/01234567-89ab-cdef-0123-456789abcdef
```

### Package A Publication

```bash
curl -X POST http://localhost:8080/v2/sync/package \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [
      {
        "type": "local_folder_path",
        "path": "./tests/fixtures/video/mp4"
      }
    ],
    "params": {
      "output_name": "publication"
    }
  }'
```

## Feature-Gated Capabilities

### OpenAPI And Scalar

- `--features openapi` exposes `/openapi.json`
- `--features "openapi scalar-docs"` additionally exposes `/docs`

### S3

Build with `--features s3` to enable:

- `s3://...` remote inputs through `remote_file_url` and `remote_folder_url`
- request-selected S3 outputs through `output.type = "s3"`

If S3 config is present in `config/service.toml` but the binary is built without the `s3` feature, startup fails.

## Common Issues

### `ffmpeg` Or `mp4fragment` Not Found

Install the external tools and ensure they are on `PATH`.

### Health Check Fails

Confirm the service is listening on the configured bind address:

```bash
curl -i http://localhost:8080/v2/health
```

### Sync Request Times Out

Increase `SERVICE__SERVER__SYNC_TIMEOUT_MS` or use the async endpoint and poll `GET /v2/jobs/{id}`.

### Request Body Too Large

Increase `SERVICE__SERVER__MAX_UPLOAD_BYTES` if your JSON request, including `in_request` payloads, exceeds the default limit.

## Next Steps

- Read the [API Quick Reference](../api/quick-reference.md)
- Read the [API Reference](../api/reference.md)
- Use the [cURL Examples](../api/curl-examples.md)
- Review the [Configuration Guide](configuration.md)
