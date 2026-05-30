---
hide:
  - toc
  - path
---

<section class="brand-hero">
  <div class="brand-hero__layout">
    <div class="brand-hero__copy">
      <span class="brand-pill">Security 4 Media Docs</span>
      <div class="brand-hero__headline">
        <h1 class="brand-hero__title">C2PA signing, packaging, and service operations.</h1>
        <div class="brand-lockup brand-lockup--light">
          <img src="images/brand/logo-en-tete-blanche.png" alt="Security 4 Media logo on a light background">
        </div>
      </div>
      <p class="brand-hero__lede">
        This documentation covers the current HTTP service surface, runtime configuration, packaging flows,
        and operational paths for local and S3-backed deployments. The emphasis is practical: build the spec,
        call the API, and run the service with the feature profile you actually need.
      </p>
      <div class="brand-hero__actions brand-card-grid">
        <a class="brand-card" href="guides/getting-started/">
          <p class="brand-card__eyebrow">Start Here</p>
          <p class="brand-card__title">Get Started</p>
          <p class="brand-card__copy">Build the docs, review the API spec, and run the service locally.</p>
        </a>
        <a class="brand-card" href="api/reference/">
          <p class="brand-card__eyebrow">Canonical Contract</p>
          <p class="brand-card__title">API Reference</p>
          <p class="brand-card__copy">Use the behavior-focused route documentation as the primary human-readable contract.</p>
        </a>
        <a class="brand-card" href="guides/running-with-s3/">
          <p class="brand-card__eyebrow">Feature-Gated Flow</p>
          <p class="brand-card__title">Run With S3</p>
          <p class="brand-card__copy">Build the service with `s3`, configure allowed buckets, and route outputs to object storage.</p>
        </a>
      </div>
    </div>
    <div class="brand-hero__visual">
      <div class="brand-lockup brand-lockup--dark">
        <img src="images/brand/logo-en-tete-noir.png" alt="Security 4 Media logo on a dark background">
      </div>
    </div>
  </div>
  <div class="brand-metrics">
    <div class="brand-metric">
      <p class="brand-metric__value">v2</p>
      <p class="brand-metric__label">Documented route surface</p>
    </div>
    <div class="brand-metric">
      <p class="brand-metric__value">OpenAPI</p>
      <p class="brand-metric__label">Synchronized from service source</p>
    </div>
    <div class="brand-metric">
      <p class="brand-metric__value">Local + S3</p>
      <p class="brand-metric__label">Operational paths covered</p>
    </div>
  </div>
</section>

## Primary Paths

<p class="brand-section-intro">
  Use these entry points when you want the shortest path to a working service, the API contract, or a deployment-specific guide.
</p>

<div class="brand-card-grid">
  <a class="brand-card" href="guides/running-local/">
    <p class="brand-card__eyebrow">Runtime</p>
    <p class="brand-card__title">Running Local</p>
    <p class="brand-card__copy">Start with local files and local output artifacts before enabling extra features.</p>
  </a>
  <a class="brand-card" href="guides/configuration/">
    <p class="brand-card__eyebrow">Configuration</p>
    <p class="brand-card__title">Configuration Guide</p>
    <p class="brand-card__copy">Review current defaults, feature-gated settings, upload limits, and startup expectations.</p>
  </a>
  <a class="brand-card" href="guides/api-docs-mode/">
    <p class="brand-card__eyebrow">Docs Tooling</p>
    <p class="brand-card__title">API Docs Mode</p>
    <p class="brand-card__copy">Understand the synchronized `api/openapi.json`, runtime `/openapi.json`, and docs build path.</p>
  </a>
</div>

## API Highlights

<p class="brand-section-intro">
  The service documentation distinguishes the human-written contract from raw examples and the generated machine-readable spec.
</p>

<div class="brand-card-grid">
  <a class="brand-card" href="api/reference/">
    <p class="brand-card__eyebrow">Authoritative</p>
    <p class="brand-card__title">API Reference</p>
    <p class="brand-card__copy">Route purpose, accepted inputs, sync versus async behavior, and current status codes.</p>
  </a>
  <a class="brand-card" href="api/quick-reference/">
    <p class="brand-card__eyebrow">Fast Scan</p>
    <p class="brand-card__title">Quick Reference</p>
    <p class="brand-card__copy">A compact map of endpoints and request categories when you already know the service.</p>
  </a>
  <a class="brand-card" href="api/curl-examples/">
    <p class="brand-card__eyebrow">Execution</p>
    <p class="brand-card__title">cURL Examples</p>
    <p class="brand-card__copy">Concrete request payloads for signing, fragmented publishing, packaging, and package+sign flows.</p>
  </a>
  <a
    class="brand-card"
    href="api/openapi.json"
    data-openapi-viewer-link
    data-openapi-spec-path="api/openapi.json"
    data-public-eyebrow="External Viewer"
    data-public-title="Swagger Editor"
    data-public-copy="Open the generated spec in Swagger Editor."
    data-local-eyebrow="Generated"
    data-local-title="Raw OpenAPI"
    data-local-copy="Open the generated OpenAPI JSON directly from this docs site."
  >
    <p class="brand-card__eyebrow">Raw OpenAPI</p>
    <p class="brand-card__title">Raw OpenAPI</p>
    <p class="brand-card__copy">Open the generated OpenAPI JSON directly from this docs site.</p>
  </a>
</div>

## Operational Paths

<div class="brand-card-grid">
  <a class="brand-card" href="guides/running-with-s3/">
    <p class="brand-card__eyebrow">Feature Profile</p>
    <p class="brand-card__title">Run With S3</p>
    <p class="brand-card__copy">Enable S3-backed input resolution and request-selected S3 outputs with the right feature flags.</p>
  </a>
  <a class="brand-card" href="guides/troubleshooting/">
    <p class="brand-card__eyebrow">Operations</p>
    <p class="brand-card__title">Troubleshooting</p>
    <p class="brand-card__copy">Use this when startup fails, external tools are missing, or runtime limits need adjustment.</p>
  </a>
</div>

## Documentation Source

Public documentation is maintained in this repository. The generated OpenAPI specification is synchronized from the private service implementation so the public API contract stays tied to the code.

Live `/openapi.json` exists only when `service-http` is built with `--features openapi`. Live `/docs` exists only when `service-http` is built with `--features "openapi scalar-docs"`.
