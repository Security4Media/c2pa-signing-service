# Running Locally

## Purpose

Use this flow when you want to run the HTTP service against local inputs and write outputs under `.artifacts/output`.

## Prerequisites

- FFmpeg on `PATH`
- Bento4 tools on `PATH`
- Rust toolchain available

## Start The Service

```bash
cargo run -p service-http
```

The default config file is `config/service.toml`.

## Verify The Service

```bash
curl -i http://localhost:8080/v2/health
```

Expected result: `200 OK` with an empty body.

## Run A Local Sync Request

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

## Outputs

- Outputs are written under `output_sinks.local.base_dir`
- The checked-in default is `./.artifacts/output`

## Related Docs

- [Getting Started](getting-started.md)
- [API Reference](../api/reference.md)
- [Configuration Guide](configuration.md)
