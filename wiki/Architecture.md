# Architecture

## Boundary

This repository provides production infrastructure and conventions without prescribing application-specific architecture.

It includes:

- Django settings driven by environment variables.
- PostgreSQL as the primary database.
- Gunicorn and Nginx deployment.
- Local and S3-compatible file storage.
- Django-native cache and email backend selection.
- Package-based feature modules.
- Health checks, structured logging, tests, and CI.

It deliberately does not include APIs, task queues, domain service layers, repositories, social authentication, or frontend frameworks without a product requirement.

## Provider Independence

Feature code uses Django interfaces rather than provider clients:

- `django.core.cache.cache` instead of Redis calls.
- `django.core.mail` instead of provider SDKs.
- Django storage APIs instead of direct S3 calls.
- Django ORM instead of database-specific access spread through modules.

Environment configuration selects implementations at the settings boundary.
Feature modules must not branch on infrastructure selectors such as `CACHE_BACKEND` or `EMAIL_BACKEND`.

## Module Layout

Product features live under `modules/`.
Large Django modules can split models, views, admin registrations, and tests into packages while retaining Django's normal discovery rules.

Use one file per cohesive concept, not automatically one file per class.
Add abstraction only when multiple concrete use cases establish a stable boundary.

## Runtime Topology

Local host development runs Django directly and infrastructure through Compose.
Local production simulation and production run Django with Gunicorn behind Nginx.

PostgreSQL remains authoritative.
Redis cache entries are optional accelerators and must never be the only copy of application data.

## Related Pages

- [Quick Start](Quick-Start)
- [Extending the Boilerplate](Extending-the-Boilerplate)
- [Deployment](Deployment)
- [Cache](Cache)
- [Email](Email)
