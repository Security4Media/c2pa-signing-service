# Running With S3

## Purpose

Use this flow when you want S3-backed inputs, request-selected S3 outputs, or both.

## Build With The Right Feature

```bash
cargo run -p service-http --features s3
```

If S3 config exists but the binary is built without `--features s3`, startup fails.

## Configure S3 Inputs

Enable `[input_resolvers.s3]` in `config/service.toml`:

```toml
[input_resolvers.s3]
region = "eu-central-1"
buckets = ["media-bucket", "publication-bucket"]
```

## Configure S3 Outputs

Add `[output_sinks.s3]`:

```toml
[output_sinks.s3]
region = "eu-central-1"
buckets = ["processed-media", "archive-media"]
base_prefix = "exports"
```

The requested `output.bucket` must be in the configured allow-list. See the [Configuration Guide](configuration.md#output_sinkss3) for the full field reference.

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
    "params": {},
    "output": {
      "type": "s3",
      "bucket": "processed-media",
      "prefix": "exports/c2pa",
      "name": "spring-campaign"
    }
  }'
```

The object key is `base_prefix / output.prefix / output.name / <per-input-leaf>`, e.g.
`exports/exports/c2pa/spring-campaign/video_c2pa.mp4`. There is no job/batch id in the
key, and reusing the same destination overwrites it.

## Common Failures

- startup error about missing feature: build with `--features s3`
- validation failure for output bucket: add the bucket to `output_sinks.s3.buckets`
- startup failure for bucket probe: verify credentials, region, endpoint, and bucket permissions

## Related Docs

- [Configuration Guide](configuration.md)
- [API Reference](../api/reference.md)
