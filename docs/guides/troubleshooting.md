# Troubleshooting

## `ffmpeg` Or `mp4fragment` Not Found

- Install the required external tools
- Verify they are on `PATH`

## Health Check Fails

- confirm the process is running
- confirm `server.bind_addr`
- test `curl -i http://localhost:8080/v2/health`

## Sync Requests Time Out

- increase `SERVICE__SERVER__SYNC_TIMEOUT_MS`
- use async submission and poll `GET /v2/jobs/{id}`

## Request Body Too Large

- increase `SERVICE__SERVER__MAX_UPLOAD_BYTES`
- this matters especially for `in_request` payloads

## S3 Config Causes Startup Failure

- build with `--features s3`
- verify the configured region, endpoint, and bucket list
- verify the output buckets are writable at startup

## Docs Build Fails

- in this public documentation repo, run `make docs-check`
- in the private implementation repo, run `make docs-sync-public` to refresh `docs/api/openapi.json`
- verify Python can create `.venv` and install Zensical

## Related Docs

- [Running Locally](running-local.md)
- [Running With S3](running-with-s3.md)
- [API Docs Mode](api-docs-mode.md)
