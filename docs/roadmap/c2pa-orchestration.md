# C2PA Orchestration

## Current State

The implementation already has job orchestration in the application layer through `BatchService`, workers, and processor dispatch. What is not yet documented is a future higher-level orchestration story for coordinating richer C2PA-specific workflows across multiple processing steps or capability areas.

## Planned Outcome

Document a clearer orchestration model for C2PA workflows that explains how multi-step processing could be composed, coordinated, and surfaced in the service and docs experience.

This roadmap item is about making orchestration a first-class documented concept, not just an internal implementation detail.

## Why It Matters

As the service grows beyond the current signing and packaging paths, readers will need a clearer explanation of how different C2PA operations relate to one another. A dedicated orchestration story would help align future API behavior, operational expectations, and architecture guidance.

## What Needs To Be In Place

- a stable vocabulary for describing orchestration versus individual processing steps
- clearer boundaries between public workflow concepts and internal worker coordination
- documentation on how orchestration interacts with sync and async execution models
- a consistent way to explain future composed flows without fragmenting the public docs

## Open Questions

- Which orchestration concepts should be public API concepts and which should remain implementation details?
- How should future orchestrated workflows be described without duplicating endpoint-level documentation?
- When new orchestration paths arrive, should they be presented as separate capabilities or as layered guides over the existing API surface?

## Related Current Docs

