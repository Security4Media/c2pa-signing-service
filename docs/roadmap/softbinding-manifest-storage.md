# Softbinding Manifest Storage

## Current State

The current docs do not describe a durable manifest-storage path for softbinding data. Internal implementation notes mention future store-oriented expansion in the infrastructure layer, but the checked-in public docs remain focused on request processing, output writing, and current runtime paths.

## Planned Outcome

Document a database-backed softbinding manifest storage capability that explains how manifest data can be stored, retrieved, and connected to future softbinding workflows.

The intended outcome is a public explanation of durable storage behavior rather than a low-level schema document. Readers should be able to understand why manifest persistence exists, what operational problem it solves, and how it fits into the service model.

## Why It Matters

Durable manifest storage would turn softbinding from a one-off processing action into a capability that can support later retrieval, operational tracking, and integration with surrounding systems. It also creates a clearer path for documenting future lookup and status workflows beyond immediate processing results.

## What Needs To Be In Place

- a clear persistence model for softbinding manifest records
- documented boundaries between transient job state and durable manifest state
- retrieval and lookup behavior that fits the public service story
- operational guidance for running the storage layer in production environments

## Open Questions

- What parts of manifest data should be durably stored versus derived on demand?
- How much of the storage model should appear in public API docs compared with operator-focused documentation?
- Should manifest storage be described first as a service capability, an integration surface, or an operational dependency?

## Related Current Docs

- [Configuration Guide](../guides/configuration.md)
