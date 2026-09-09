# Configuration Guide

This service uses a typed top-level TOML configuration file.

## Overview

Configuration is split into two layers:

- `config/service.toml`
  - service bootstrap settings
  - server parameters
  - worker parameters
  - input resolver settings
  - output sink settings
  - paths to processor-specific TOML files
- specialized processor TOMLs
  - `config/c2pa/*.toml`
  - `config/media-packager/*.toml`

The service loads `config/service.toml` by default. Set `SERVICE_CONFIG_PATH` to point at a different file.

## Service Config

Example:

```toml
[server]
bind_addr = "0.0.0.0:8080"
max_upload_bytes = 52428800
sync_timeout_ms = 120000
sync_poll_interval_ms = 250

[worker]
queue_capacity = 128
max_concurrent_batches = 4
max_files_parallel = 4

[input_resolvers.s3]
# profile = "my-aws-profile"
force_path_style = false
buckets = []

[output_sinks.local]
base_dir = "./.artifacts/output"

[output_sinks.s3]
# region = "eu-central-1"
# force_path_style = false
# buckets = ["processed-media", "archive-media"]
# base_prefix = "exports"

[processors.c2pa]
sdk_settings_path = "config/c2pa/default_c2pa_sdk_settings.toml"

[processors.media_packager]
pipeline_config_path = "config/media-packager/media_packager_pipeline.toml"
```

## Sections

### `server`

- `bind_addr`: address and port for the HTTP server
- `max_upload_bytes`: maximum HTTP request body size accepted by Axum
- `sync_timeout_ms`: sync endpoint timeout
- `sync_poll_interval_ms`: sync endpoint polling interval

### `worker`

- `queue_capacity`: job queue size
- `max_concurrent_batches`: maximum batches processed in parallel
- `max_files_parallel`: per-batch input parallelism, applied to every batch (requests cannot override it)

### `input_resolvers.s3`

- presence of this section enables S3 resolver bootstrap
- `profile`: optional AWS shared config profile; when omitted the default credential chain is used
- `region`: optional AWS region
- `endpoint_url`: optional custom endpoint for MinIO/LocalStack
- `force_path_style`: enable path-style addressing
- `buckets`: allowed buckets and startup validation targets

### `output_sinks.local`

- `base_dir`: base directory for persisted outputs
- `naming`: file-leaf naming mode for single-file outputs written to this sink; `"derived"` (default, appends `_c2pa`) or `"in_place"` (keep the input filename). Folder/publication outputs always use the input folder name.

### `output_sinks.s3`

- optional output sink configuration under the existing `s3` feature
- `profile`: optional AWS shared config profile
- `region`: optional AWS region
- `endpoint_url`: optional custom S3-compatible endpoint
- `force_path_style`: enable path-style addressing
- `buckets`: writable bucket allow-list for request-selected S3 outputs
- `base_prefix`: optional shared prefix prepended to every uploaded object key
- `naming`: file-leaf naming mode for single-file outputs, same values and default as `output_sinks.local.naming`

Behavior:

- there is no default S3 output bucket
- a request selects S3 output with `output.type = "s3"` and a `bucket`; `output.type = "local"` (or omitting `output`) targets the local sink instead
- only configured buckets are accepted
- configured output buckets are write-probed during startup
- object keys are composed as `base_prefix / output.prefix / output.name / <per-input-leaf>`; there is no job/batch id segment. `output.prefix = "/"` (or omitted) writes directly under `base_prefix`; if no `base_prefix` is configured, keys start at the bucket root. Reusing a destination overwrites it.

### `processors`

These sections reference specialized processor configuration files instead of inlining their internals:

- `processors.c2pa.sdk_settings_path`
- `processors.media_packager.pipeline_config_path`

## Feature Flags

- `openapi`: exposes `/openapi.json`
- `scalar-docs`: extends `openapi` and exposes `/docs`
- `s3`: enables S3-backed input resolvers and request-selectable S3 outputs

The synchronized public OpenAPI file is generated from the private service implementation using the documentation feature profile, which enables both `openapi` and `s3`.

If `[input_resolvers.s3]` or `[output_sinks.s3]` is configured without building
the service with `--features s3`, startup fails.

## Request Input Types

The current request model is provider-agnostic:

- `local_file_path`
- `local_folder_path`
- `remote_file_url`
- `remote_folder_url`

Examples:

```json
{"type": "remote_file_url", "url": "https://example.com/video.mp4"}
{"type": "remote_file_url", "url": "s3://media-bucket/input/video.mp4"}
{"type": "remote_folder_url", "url": "s3://media-bucket/publication/42/"}
```

## Request Output Types

The `output` section selects the destination and placement. Supported types:

- `local` — writes under `output_sinks.local.base_dir` on the service host (dev/self-host). Omitting `output` is equivalent to `{"type": "local"}` with no fields.
- `s3` — writes to object storage; requires the `s3` build feature and a configured bucket.

Both accept optional `prefix` and `name`. The file-leaf naming mode is not a request field; it is configured per output sink (`output_sinks.*.naming`, see above). See [Output Selection](../api/reference.md#output-selection) for the full contract.

Examples:

```json
null
{"type": "local", "name": "spring-campaign"}
{"type": "s3", "bucket": "processed-media", "prefix": "c2pa/video", "name": "spring-campaign"}
{"type": "s3", "bucket": "processed-media", "prefix": "/"}
```
