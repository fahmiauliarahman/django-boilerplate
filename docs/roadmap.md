# Boilerplate Roadmap

This document lists recommended additions to the Django boilerplate in priority order.
Add features only when the project needs them.

## Progress

- [x] Continuous integration
- [x] Health check endpoint
- [x] Starter test suite
- [ ] Structured logging
- [ ] Backup and restore commands
- [ ] Development Compose override, if needed
- [ ] Authentication example, when requirements exist
- [ ] API example, when requirements exist

## 1. Continuous Integration

Add a CI workflow that runs for every pull request and protected branch update.

The workflow should:

- Install dependencies from `uv.lock`.
- Run `python manage.py check`.
- Run `python manage.py test`.
- Check for missing migrations with `python manage.py makemigrations --check --dry-run`.
- Validate `docker compose config`.
- Build the production Docker image.

Complete when broken checks, missing migrations, failing tests, and invalid Docker builds block merging.

## 2. Health Check Endpoint

Add an endpoint such as `/health/` for container and platform monitoring.

The endpoint should:

- Return HTTP 200 when Django is running.
- Verify the database connection when used as a readiness check.
- Avoid exposing secrets, versions, or internal error details.
- Be used by the Compose `web` health check.

Complete when Docker can distinguish a running process from an application ready to receive traffic.

## 3. Starter Test Suite

The repository contains a runnable starter test suite.

Add small tests covering:

- Root URL behavior.
- Admin login page availability.
- Health check behavior.
- One model creation flow.
- One authenticated or permission-protected flow when authentication features exist.

Complete when `make test` runs meaningful tests and catches a broken request path or database integration.

## 4. Structured Logging

Configure Django and Gunicorn to write logs to stdout and stderr for container log collection.

Logging should include:

- Timestamp.
- Severity.
- Logger name.
- Request method and path where applicable.
- Exception traceback for server errors.

Do not log passwords, secret keys, authorization headers, cookies, or personal data.

Complete when `docker compose logs web` provides enough information to diagnose failed requests and startup errors.

## 5. Backup and Restore Commands

Document and automate PostgreSQL and uploaded-media recovery.

Add commands for:

- Creating a timestamped PostgreSQL dump.
- Restoring a selected dump.
- Backing up the local media volume.
- Verifying that a backup can be restored.

Complete when a fresh deployment can be restored from documented backup artifacts.

## 6. Development Compose Override

Add development-specific Compose configuration only if contributors use containers for daily development.

It may provide:

- Django development server with auto-reload.
- Source bind mount.
- Debug mode.
- Exposed PostgreSQL port when local database tools require it.

Keep production configuration free from source mounts and development dependencies.

Complete when local code changes reload without rebuilding while production behavior remains unchanged.

## 7. Authentication Example

Add authentication only when product requirements are known.

Possible scope:

- Custom user model created before initial production migrations.
- Login and logout flows.
- Password reset flow.
- Permission-protected view example.
- Tests for anonymous and authenticated access.

Prefer Django's built-in authentication before adding third-party packages.

Complete when one protected feature demonstrates the project's authorization pattern.

## 8. API Example

Add an API framework only when the application needs an external or JavaScript-facing API.

Choose one framework based on project requirements:

- Django Ninja for typed, compact APIs.
- Django REST Framework for broad ecosystem support and advanced API features.

The example should include:

- One list/create endpoint.
- Input validation.
- Authentication or explicit public access.
- Consistent error responses.
- Request tests.
- Generated or maintained API documentation.

Complete when new API modules have one clear pattern to follow.

## Recommended Order

1. Continuous integration.
2. Health check endpoint.
3. Starter test suite.
4. Structured logging.
5. Backup and restore commands.
6. Development Compose override, if needed.
7. Authentication example, when requirements exist.
8. API example, when requirements exist.
