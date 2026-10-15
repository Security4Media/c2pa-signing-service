# API Docs Mode

## Purpose

Use this page to understand the two documentation surfaces for the service: runtime API docs exposed by the service binary and the static public documentation site.

## Runtime OpenAPI Endpoints

Enable the runtime raw spec when running the service from a source checkout or service build:

```bash
cargo run -p service-http --features openapi
```

Runtime endpoint:

- `/openapi.json`

Enable Scalar as well:

```bash
cargo run -p service-http --features "openapi scalar-docs"
```

Additional runtime endpoint:

- `/docs`

Both stay open in a build with `oidc`. To send test requests from `/docs` to such a build, choose the `bearer`
authentication and paste an access token ([Authentication](authentication.md)); the page does not store it.

## Public Docs-Site Raw Spec

The public docs site serves a generated raw spec at `docs/api/openapi.json`.

That file is generated from the private service implementation and synchronized into this repository. From the private implementation checkout, run:

```bash
make docs-sync-public
```

The generation builds with the `openapi` feature only: the schemas do not depend on `s3` or the other runtime features.
The generated file documents authentication in every case, because it describes the API as deployed with `oidc`.

## Build The Public Docs Site

From this public documentation repository:

```bash
make docs
```

## Preview The Public Docs Site

```bash
make docs-serve
```

## Swagger Editor Card

The docs homepage includes a Swagger Editor card that can preload `api/openapi.json` when the docs site is hosted at a public URL.

When you browse the docs locally, the card opens the raw generated asset at `api/openapi.json` instead.

## Related Docs

- [API Reference](../api/reference.md)
- [Documentation Index](../index.md)
