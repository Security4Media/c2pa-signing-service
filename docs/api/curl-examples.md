# API cURL Examples

Examples in this page target the current v2 HTTP surface implemented by `service-http`.
For the canonical route contract, see [API Reference](reference.md).

## Health Check

```bash
curl -i http://localhost:8080/v2/health
```

Expected status: `200 OK`

## C2PA Video Signing

### Async

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
    "params": {
      "output_name": "signed-video.mp4",
      "options": {
        "timeout_ms": 2500,
        "in_place": false
      }
    },
    "options": {
      "max_files_parallel": 2
    }
  }'
```

### Sync

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

## C2PA Fragmented Signing

### Async

```bash
curl -X POST http://localhost:8080/v2/c2pa/fragmented \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [
      {
        "type": "remote_folder_url",
        "url": "s3://media-bucket/publication/"
      }
    ],
    "params": {
      "publication_name": "demo-publication",
      "playlist_pattern": "**/*.m3u8",
      "init_pattern": "**/init*.mp4",
      "frag_pattern": "seg*.m4s"
    }
  }'
```

### Sync

```bash
curl -X POST http://localhost:8080/v2/sync/c2pa/fragmented \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [
      {
        "type": "local_folder_path",
        "path": "./tests/fixtures/hls/publication"
      }
    ],
    "params": {
      "publication_name": "signed-publication",
      "playlist_pattern": "**/*.m3u8",
      "init_pattern": "**/init*.mp4",
      "frag_pattern": "seg*.m4s"
    }
  }'
```

## Media Packaging

### Async

```bash
curl -X POST http://localhost:8080/v2/package \
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

### Sync

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

## Package And Sign

### Async

```bash
curl -X POST http://localhost:8080/v2/c2pa/package \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [
      {
        "type": "local_folder_path",
        "path": "./tests/fixtures/video/mp4"
      }
    ],
    "params": {
      "output_name": "publication",
      "playlist_pattern": "**/*.m3u8",
      "init_pattern": "**/init*.mp4",
      "frag_pattern": "seg*.m4s"
    }
  }'
```

### Sync

```bash
curl -X POST http://localhost:8080/v2/sync/c2pa/package \
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

## In-Request File Payload

The request model also supports base64-embedded file inputs:

```bash
curl -X POST http://localhost:8080/v2/sync/c2pa/video \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [
      {
        "type": "in_request",
        "media_type": "video/mp4",
        "data_base64": "AA==",
        "filename": "clip.mp4"
      }
    ],
    "params": {}
  }'
```

## Request-Selected S3 Output

Available only when the service is built with `--features s3` and the target bucket is configured in `output_sinks.s3.buckets`.

```bash
curl -X POST http://localhost:8080/v2/c2pa/video \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [
      {
        "type": "remote_file_url",
        "url": "s3://media-bucket/input/video.mp4",
        "filename_hint": "video.mp4"
      }
    ],
    "params": {
      "output_name": "signed-video.mp4"
    },
    "output": {
      "type": "s3",
      "bucket": "processed-media",
      "prefix": "exports/c2pa"
    }
  }'
```

## Job Status Query

After an async submission:

```bash
curl http://localhost:8080/v2/jobs/01234567-89ab-cdef-0123-456789abcdef
```

## Placeholder Endpoints

The watermark endpoints are visible but not implemented:

```bash
curl -i -X POST http://localhost:8080/v2/watermark
curl -i http://localhost:8080/v2/watermark/wm-1
```

Expected status: `501 Not Implemented`

## Example Responses

### Async Submission

```json
{
  "job_id": "01234567-89ab-cdef-0123-456789abcdef",
  "status": "queued"
}
```

### Completed Sync Response

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

### Polling Response

```json
{
  "job_id": "01234567-89ab-cdef-0123-456789abcdef",
  "status": "running",
  "results": [],
  "timing": {
    "queued_at": "2026-04-09T08:00:00Z",
    "started_at": "2026-04-09T08:00:01Z"
  }
}
```

## Notes

- Async responses do not include a `status_url`; poll `GET /v2/jobs/{id}`.
- Sync endpoints return `408` if the job does not finish before `server.sync_timeout_ms`.
- Omitting `output` uses the configured local sink.
- There is no `local_path` request output type.

## See Also

- [API Reference](reference.md)
- [Quick Reference](quick-reference.md)
- [Configuration Guide](../guides/configuration.md)
