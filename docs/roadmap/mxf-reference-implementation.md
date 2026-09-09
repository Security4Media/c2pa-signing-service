# MXF Reference Implementation

## Current State

The current public HTTP surface documents C2PA signing for monolithic video, fragmented/HLS-style publications, and audio. MXF (Material Exchange Format, SMPTE ST 377) is the container format most commonly used in broadcast production and exchange workflows, and it is not yet part of the documented signing surface.

## Planned Outcome

Document a reference implementation for applying C2PA provenance to MXF assets, covering how broadcast-style production and exchange workflows can carry authenticity data end to end.

The Security4Media authenticity group is positioned to contribute to this reference implementation, drawing on broadcaster-specific workflow requirements that a general-purpose signing service wouldn't otherwise capture.

## Why It Matters

MXF is the working format for a large share of broadcast production and archival workflows. A documented, broadcast-aware reference implementation would extend the project's authenticity story from general-purpose media signing into the container format public media organizations actually use in production.

## What Needs To Be In Place

- a clear scope for what "C2PA-in-MXF" covers (essence-level signing, wrapper-level manifest embedding, or both)
- alignment with the C2PA specification's guidance on MXF (where it exists) and with broadcast industry practice
- a way for interested organizations to engage before the work is public, since this starts as a collaborative effort rather than a documented capability

## Open Questions

- What is the right scope for a first reference implementation: a single production workflow, or a broader set of MXF operating patterns?
- How should this work be sequenced relative to the [C2PA Orchestration](c2pa-orchestration.md) and [C2PA Image Signing](c2pa-image-signing.md) roadmap areas?
- What governance applies to a reference implementation developed with external contributors?

If you or your organization wants to contribute to or shape this work, [contact Security4Media](https://security4media.org/membership/) to get involved.

## Related Current Docs

- [API Reference](../api/reference.md)
- [Getting Started](../guides/getting-started.md)
- [C2PA Orchestration](c2pa-orchestration.md)
