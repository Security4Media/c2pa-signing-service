# Configuration Guide

This service uses a typed top-level configuration file plus environment overrides.

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
default_max_files_parallel = 4

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
- `default_max_files_parallel`: default per-batch input parallelism

### `input_resolvers.s3`

- presence of this section enables S3 resolver bootstrap
- `profile`: optional AWS shared config profile; when omitted the default credential chain is used
- `region`: optional AWS region
- `endpoint_url`: optional custom endpoint for MinIO/LocalStack
- `force_path_style`: enable path-style addressing
- `buckets`: allowed buckets and startup validation targets

### `output_sinks.local`

- `base_dir`: base directory for persisted outputs

### `output_sinks.s3`

- optional output sink configuration under the existing `s3` feature
- `profile`: optional AWS shared config profile
- `region`: optional AWS region
- `endpoint_url`: optional custom S3-compatible endpoint
- `force_path_style`: enable path-style addressing
- `buckets`: writable bucket allow-list for request-selected S3 outputs
- `base_prefix`: optional shared prefix prepended to every uploaded object key

Behavior:

- there is no default S3 output bucket
- request payloads must explicitly choose `output.type = "s3"` with `bucket` and `prefix`
- only configured buckets are accepted
- configured output buckets are write-probed during startup
- `prefix = "/"` writes directly under the configured `base_prefix` root; if no `base_prefix` is configured, objects are written at the bucket root under the batch prefix

### `processors`

These sections reference specialized processor configuration files instead of inlining their internals:

- `processors.c2pa.sdk_settings_path`
- `processors.media_packager.pipeline_config_path`

## Environment Overrides

Environment variables override `service.toml` values using the `SERVICE__...` prefix.

Examples:

```bash
export SERVICE_CONFIG_PATH=config/service.prod.toml
export SERVICE__SERVER__BIND_ADDR=0.0.0.0:9090
export SERVICE__SERVER__SYNC_TIMEOUT_MS=90000
export SERVICE__WORKER__QUEUE_CAPACITY=256
export SERVICE__INPUT_RESOLVERS__S3__PROFILE=my-aws-profile
export SERVICE__INPUT_RESOLVERS__S3__REGION=eu-central-1
export SERVICE__INPUT_RESOLVERS__S3__BUCKETS=media-a,media-b
export SERVICE__OUTPUT_SINKS__S3__REGION=eu-central-1
export SERVICE__OUTPUT_SINKS__S3__BUCKETS=processed-media,archive-media
export SERVICE__OUTPUT_SINKS__S3__BASE_PREFIX=exports
```

Use environment variables for:

- environment-specific operational values
- deployment overrides
- secret references and cloud runtime integration

Keep structured defaults in `service.toml`.

## Container and Cloud Usage

Recommended pattern:

- mount `config/service.toml` from a ConfigMap or baked-in image config
- mount processor-specific TOMLs separately if needed
- use `SERVICE__...` for deployment-specific overrides
- use the AWS default credential chain for S3 access instead of storing credentials in TOML

This works well for:

- Docker
- Kubernetes
- GitHub Actions
- AWS-hosted deployments

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
- `in_request`

Examples:

```json
{"type": "remote_file_url", "url": "https://example.com/video.mp4"}
{"type": "remote_file_url", "url": "s3://media-bucket/input/video.mp4"}
{"type": "remote_folder_url", "url": "s3://media-bucket/publication/42/"}
```

## Request Output Types

Current supported output types:

- configured local output by omitting the `output` field
- `s3` when the service is built with the `s3` feature and output buckets are configured

Examples:

```json
null
{"type": "s3", "bucket": "processed-media", "prefix": "c2pa/video"}
{"type": "s3", "bucket": "processed-media", "prefix": "/"}
```
