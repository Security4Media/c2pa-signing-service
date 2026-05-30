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
  - `params.output_name`: optional
  - `params.options.timeout_ms`: optional
  - `params.options.in_place`: optional
  - `output`: optional; omitted means configured local sink
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
  - `publication_name`
  - `playlist_pattern`
  - `init_pattern`
  - `frag_pattern`
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
- Required params:
  - `output_name`
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
- Required params:
  - `output_name`
- Optional params:
  - `playlist_pattern`
  - `init_pattern`
  - `frag_pattern`
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

## Output Selection

- If `output` is omitted or `null`, artifacts go to the configured local sink rooted at `output_sinks.local.base_dir`.
- `output.type = "s3"` is available only when the service is built with `--features s3` and the requested bucket is present in `output_sinks.s3.buckets`.
- There is no supported request output type named `local_path`.

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
