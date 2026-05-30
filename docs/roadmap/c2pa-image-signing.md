# C2PA Image Signing

## Current State

The current public HTTP surface documents C2PA signing for monolithic video assets and fragmented/HLS-style publications. The docs do not yet describe an image-oriented signing workflow or a separate image-focused request path.

## Planned Outcome

Document a dedicated C2PA image-signing capability that explains how image assets would be submitted, signed, and returned through the service.

The goal is to make image authenticity a first-class documented capability alongside the current video-focused flows.

## Why It Matters

Image signing is a natural extension of the project’s authenticity story. It would broaden the service from video-heavy workflows into a more general C2PA platform and make the public docs easier to position for media types beyond packaged video delivery.

## What Needs To Be In Place

- a clear public distinction between image signing and existing video-signing flows
- request and response semantics that fit the current sync and async job model
- documentation on supported image inputs, outputs, and artifact expectations
- clarity on whether image signing stands alone or shares capability patterns with future orchestration work

## Open Questions

- Should image signing appear as its own primary endpoint family or as a media-specific variant of the existing C2PA request model?
- How closely should image requests mirror the current `c2pa/video` wire shape?
- What parts of image-signing behavior belong in the public HTTP docs versus media-specific guides?

## Related Current Docs

- [API Reference](../api/reference.md)
- [Getting Started](../guides/getting-started.md)
- [C2PA Orchestration](c2pa-orchestration.md)
