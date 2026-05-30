# Expanded Resolvers And Sinks

## Current State

The current docs cover local filesystem paths, HTTP-backed remote URLs, and S3-oriented remote input and output behavior. The public docs do not yet describe broader provider coverage such as GCS, Azure-backed storage, or database-oriented integration paths.

## Planned Outcome

Document a broader resolver and sink story that explains how the service could expand beyond today’s local, HTTP, and S3 patterns into additional cloud and data-platform integrations.

The intended outcome is a public explanation of integration breadth, not a detailed provider-by-provider setup guide yet.

## Why It Matters

Broader resolver and sink coverage makes the service easier to adopt in heterogeneous infrastructure environments. It also strengthens the platform story by making the input and output model less tied to one object-storage profile.

## What Needs To Be In Place

- a consistent public vocabulary for provider-agnostic versus provider-specific inputs and outputs
- documentation boundaries between generic resolver/sink behavior and provider-specific deployment guides
- clarity on how database-oriented integrations fit the current request-processing model
- a repeatable way to describe feature-gated or optional provider support

## Open Questions

- Which provider integrations should be presented as first-class roadmap items versus examples of a more generic plugin model?
- Should database-based integrations be described as resolvers, sinks, or a different integration category entirely?
- How much provider-specific detail belongs in roadmap pages before dedicated operational guides exist?

## Related Current Docs

- [Configuration Guide](../guides/configuration.md)
- [Running With S3](../guides/running-with-s3.md)
- [Multi-Cloud Deployment Guides](multi-cloud-deployment-guides.md)
