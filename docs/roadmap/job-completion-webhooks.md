# Job Completion Webhooks

## Current State

The current async job model is documented as submit-plus-poll. Clients submit work, receive a queued job response, and use `GET /v2/jobs/{id}` to observe progress and completion.

## Planned Outcome

Document a webhook-based completion-notification capability that explains how async job results could be pushed to external systems instead of requiring polling alone.

The roadmap goal is to describe callback-driven job completion as a service capability layered over the current async execution model.

## Why It Matters

Webhook notifications reduce integration friction for external systems that need completion events without repeated polling. They also move the service closer to event-driven operational patterns that are common in production media pipelines and partner integrations.

## What Needs To Be In Place

- a clear relationship between polling and callback-based completion
- documented registration or per-request callback behavior
- delivery expectations for success, failure, retries, and idempotency
- security guidance for authenticating outbound notifications

## Open Questions

- Should webhook targets be request-scoped, account-scoped, or deployment-scoped?
- What completion states should trigger notifications: success only, or all terminal states?
- How should retries and delivery failures be described without overcommitting to a final transport contract?

## Related Current Docs

- [API Reference](../api/reference.md)
- [Getting Started](../guides/getting-started.md)
- [Authentication And Authorization](authentication-and-authorization.md)
