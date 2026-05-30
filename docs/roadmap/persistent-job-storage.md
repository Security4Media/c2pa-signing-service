# Persistent Job Storage

## Current State

The current public docs describe job submission, polling, and lifecycle behavior without a durable production storage story. The internal implementation notes hint at future SQLite and PostgreSQL-backed job stores, but the public service story remains centered on transient in-memory lifecycle tracking.

## Planned Outcome

Document a persistent job-storage capability that explains how job history, terminal state, and operational recovery could be preserved across restarts and longer-running deployments.

This roadmap item is about durable job-state behavior, not just naming a database technology.

## Why It Matters

Persistent job storage is a key step toward production-grade operation. It affects observability, restart resilience, support workflows, and any future integration features that depend on durable async state such as webhooks, dashboards, or historical audit views.

## What Needs To Be In Place

- a documented distinction between transient worker state and durable job state
- a clear public story for retention, lookup, and post-restart behavior
- operator guidance for running a database-backed store
- boundaries between job-state persistence and future manifest or media metadata persistence

## Open Questions

- Should persistent storage be presented first as an operational deployment option or as a core service capability?
- What job history guarantees should appear in public docs before a storage backend is fully settled?
- How should SQLite and PostgreSQL be positioned: interchangeable options, or different deployment tiers?

## Related Current Docs

- [API Reference](../api/reference.md)
- [Softbinding Manifest Storage](softbinding-manifest-storage.md)
