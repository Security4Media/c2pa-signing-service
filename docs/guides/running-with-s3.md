# Running With S3

## Purpose

Use this flow when you want S3-backed inputs, request-selected S3 outputs, or both.

## Build With The Right Feature

```bash
cargo run -p service-http --features s3
```

If S3 config exists but the binary is built without `--features s3`, startup fails.

## Configure S3 Inputs

Enable `[input_resolvers.s3]` in `config/service.toml` or by environment override:

```bash
export SERVICE__INPUT_RESOLVERS__S3__REGION=eu-central-1
export SERVICE__INPUT_RESOLVERS__S3__BUCKETS=media-bucket,publication-bucket
```

## Configure S3 Outputs

Add or override `output_sinks.s3`:

```bash
export SERVICE__OUTPUT_SINKS__S3__REGION=eu-central-1
export SERVICE__OUTPUT_SINKS__S3__BUCKETS=processed-media,archive-media
export SERVICE__OUTPUT_SINKS__S3__BASE_PREFIX=exports
```

The requested `output.bucket` must be in the configured allow-list.

## Example Request

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

## Common Failures

- startup error about missing feature: build with `--features s3`
- validation failure for output bucket: add the bucket to `output_sinks.s3.buckets`
- startup failure for bucket probe: verify credentials, region, endpoint, and bucket permissions

## Related Docs

- [Configuration Guide](configuration.md)
- [API Reference](../api/reference.md)
