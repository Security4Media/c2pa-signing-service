# Authentication And Authorization

## Current State

The current public docs describe the processing API and runtime behavior without any documented authentication or authorization model. The service surface is currently presented as an unprotected processing API rather than a caller-scoped platform surface.

## Planned Outcome

Document a future authentication and authorization model that explains how callers identify themselves, how access is enforced, and how protected operations or capability scopes are expected to work.

The intended result is a public security and access-control story, not just an internal middleware note.

## Why It Matters

As the service grows toward production-facing and partner-facing deployments, access control becomes part of the product contract. It affects how teams expose the service, how they separate tenants or roles, and how they reason about protected capabilities such as callbacks, storage access, and future administrative operations.

## What Needs To Be In Place

- a clear public identity model for service callers
- documentation boundaries between authentication, authorization, and deployment-layer protections
- a consistent story for how protected access fits current sync and async job flows
- operator guidance on configuration, secrets, and enforcement points

## Open Questions

- Should the public auth story be token-based only, or should it remain deployment-model agnostic in early docs?
- Which operations need differentiated authorization scope versus simple authenticated access?
- How much of the access-control model belongs in the API reference compared with operational guides?

## Related Current Docs

- [API Reference](../api/reference.md)
- [Configuration Guide](../guides/configuration.md)
- [Multi-Cloud Deployment Guides](multi-cloud-deployment-guides.md)
