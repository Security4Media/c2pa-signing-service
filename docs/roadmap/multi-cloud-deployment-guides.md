# Multi-Cloud Deployment Guides

## Current State

The current docs explain how to run the service locally and how to enable S3-backed inputs and outputs. They do not yet provide platform-oriented deployment guidance for running the service across a broader set of cloud environments.

## Planned Outcome

Document a multi-cloud deployment story that explains how to package, configure, and operate the service across different hosting environments without assuming a single platform path.

The goal is a practical set of deployment guides that help operators move from local or S3-backed experimentation toward repeatable cloud-hosted operation.

## Why It Matters

Public deployment guidance makes the project easier to evaluate, operate, and integrate into different runtime environments. It also helps separate core service behavior from environment-specific operational choices, which is important for adoption beyond one infrastructure profile.

## What Needs To Be In Place

- a clear baseline deployment model for the HTTP service and its external tool dependencies
- guidance for configuration, secrets, storage, and network exposure in hosted environments
- documentation boundaries between generic operational requirements and platform-specific examples
- a repeatable way to explain feature flags and optional components in deployment contexts

## Open Questions

- Which deployment concerns should stay generic across platforms, and which need platform-specific runbooks?
- How much production guidance belongs in the public docs versus environment-specific implementation notes?
- What is the minimum operational baseline that every cloud deployment guide should share?

## Related Current Docs

- [Getting Started](../guides/getting-started.md)
- [Running Local](../guides/running-local.md)
- [Running With S3](../guides/running-with-s3.md)
- [Configuration Guide](../guides/configuration.md)
