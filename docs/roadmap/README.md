# Roadmap

This roadmap highlights the next capability areas we expect to document and expand in the C2PA Signing Service project.

It is a public-facing view of the direction of the docs and service surface, not a dated delivery plan. The topics below are intentionally unordered and should be read as planned capability areas rather than release commitments.

## Current Scope

Today, the docs cover the current service surface, runtime configuration, local operation, S3-backed operation.

The roadmap extends that foundation into ten areas where the current docs and public surface are intentionally incomplete:

- [Softbinding Insertion](softbinding-insertion.md): move from placeholder watermark endpoints toward a documented softbinding insertion capability
- [Softbinding Manifest Storage](softbinding-manifest-storage.md): describe how durable manifest storage could support lookup, retrieval, and operational workflows
- [C2PA Orchestration](c2pa-orchestration.md): document how higher-level orchestration could shape multi-step C2PA flows beyond the current request-processing model
- [Multi-Cloud Deployment Guides](multi-cloud-deployment-guides.md): extend the current local and S3-backed operational guidance into broader deployment patterns
- [C2PA Image Signing](c2pa-image-signing.md): extend the current authenticity story beyond video and fragmented media into image-oriented signing workflows
- [Authentication And Authorization](authentication-and-authorization.md): describe how access control and caller identity could shape protected service usage
- [Job Completion Webhooks](job-completion-webhooks.md): document a callback-driven alternative to polling for async job completion
- [Expanded Resolvers And Sinks](expanded-resolvers-and-sinks.md): describe broader cloud and database-oriented input and output integration paths
- [Persistent Job Storage](persistent-job-storage.md): explain how durable SQLite/PostgreSQL-backed job state could replace in-memory-only lifecycle tracking
- [Live DASH Streaming](live-dash-streaming.md): extend the packaging roadmap toward live DASH-oriented workflows beyond today’s batch processing model

## How To Read This Section

Each roadmap page follows the same format:

- a short note on the current repo or docs state
- the planned outcome
- why the area matters
- what likely needs to be in place first
- the main open questions still shaping the final docs

## Related Current Docs

- [Getting Started](../guides/getting-started.md)
- [Running Local](../guides/running-local.md)
- [Running With S3](../guides/running-with-s3.md)
- [API Reference](../api/reference.md)
