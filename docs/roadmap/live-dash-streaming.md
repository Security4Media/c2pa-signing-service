# Live DASH Streaming

## Current State

The current docs cover packaging and fragmented-media processing in a batch-oriented way. They do not yet describe a live DASH streaming model or how live packaging would differ from the current file- and folder-driven flows.

## Planned Outcome

Document a live DASH streaming capability that explains how the service could support live packaging-oriented workflows in addition to today’s offline or batch-style media preparation.

The roadmap goal is to frame live DASH as a future service capability, not merely a low-level media-packager option.

## Why It Matters

Live streaming support would meaningfully extend the project beyond static asset preparation into more operationally demanding media-delivery scenarios. It would also clarify how the platform could evolve from file-based processing toward time-sensitive streaming workflows.

## What Needs To Be In Place

- a public distinction between batch packaging and live streaming workflows
- clear lifecycle expectations for long-running or continuously updated jobs
- documentation on how live DASH would relate to future webhook, auth, and persistence work
- a stable vocabulary for live publication state, outputs, and operational control

## Open Questions

- Should live DASH be described as a new primary workflow or as an extension of existing packaging behavior?
- How much of the live-control surface belongs in the public API contract versus operator-focused documentation?
- What runtime guarantees need to be defined before live DASH can be documented credibly?

## Related Current Docs

- [API Reference](../api/reference.md)
- [Job Completion Webhooks](job-completion-webhooks.md)
