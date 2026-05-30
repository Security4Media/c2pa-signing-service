# Softbinding Insertion

## Current State

The current public HTTP surface exposes watermark endpoints only as placeholders. The API reference and handler quick reference both describe them as reserved for future softbinding work and currently returning `501 Not Implemented`.

## Planned Outcome

Document a real softbinding insertion capability that explains how clients submit a request, what kind of media and metadata inputs are expected, and what output or job state they should receive in return.

The target is not only a new endpoint description, but a clear public explanation of where softbinding fits within the broader C2PA processing model.

## Why It Matters

Softbinding is one of the clearest gaps between the current documented API surface and the future direction implied by the placeholder routes. Making it a documented capability would help external readers understand how the project intends to handle watermark-oriented or softbinding-oriented workflows alongside signing and packaging.

## What Needs To Be In Place

- a concrete softbinding processing model instead of placeholder route behavior
- request and response semantics that fit the existing sync and async job conventions
- documentation on input expectations, output artifacts, and failure modes
- clarity on how softbinding relates to existing C2PA signing and packaging flows

## Open Questions

- Should softbinding be presented as its own primary workflow or as one step within a broader C2PA pipeline?
- What parts of the future softbinding surface belong in the public HTTP contract versus implementation-specific docs?
- How closely should the softbinding request model mirror the existing video-signing request patterns?

## Related Current Docs

- [API Reference](../api/reference.md)
