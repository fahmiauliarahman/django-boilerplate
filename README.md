# Django Production Boilerplate

Start building product features instead of rebuilding Django infrastructure.

This template provides a practical Django foundation for local development and production deployment, with deliberate defaults and no application-specific architecture to remove.

## Why Use This Template?

- **Production-ready foundation.** Run Django behind Gunicorn and Nginx with HTTPS, secure production settings, health checks, and structured logs.
- **Fast local setup.** Install locked dependencies with uv, use PostgreSQL from day one, and run common tasks through a small Makefile.
- **Deployment flexibility.** Ship with Docker Compose or deploy directly to a Linux host with systemd.
- **Storage that can grow.** Keep uploads on local disk or switch to Amazon S3, Cloudflare R2, MinIO, or another S3-compatible service through environment configuration.
- **Email without provider lock-in.** Develop against Mailpit and use any SMTP provider in production.
- **A scalable project layout.** Organize features as package-based modules without speculative service, repository, or utility layers.
- **Confidence by default.** CI checks Django configuration, tests, migrations, Compose configuration, and the production image on every change.

## Included

- Python 3.14, Django 6.0, and PostgreSQL 18
- uv dependency management with a committed lockfile
- Django Unfold admin interface
- Gunicorn, Nginx, WhiteNoise, and HTTPS-ready Compose deployment
- Local and S3-compatible media storage
- SMTP email and local Mailpit inbox
- Database-aware health check endpoint
- Structured container logging
- Starter tests and GitHub Actions CI
- Environment-based configuration with production security defaults
- Module generator for package-based Django apps

## Quick Start

Install Python through [mise](https://mise.jdx.dev/) or your preferred version manager, then run:

```sh
mise install
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

Open <http://127.0.0.1:8000/>.

Create an administrator when needed:

```sh
uv run python manage.py createsuperuser
```

Run the project checks:

```sh
make test
make check
```

Use `make help` to list all available development commands.

## Build Your Application

Feature code lives under `modules/`.
Create a package-based module with:

```sh
make create-app NAME=blog
```

The template intentionally leaves product decisions such as APIs, background jobs, caching, and social authentication to your application.

See [Extend the boilerplate](docs/extending.md) for a complete feature walkthrough.

## Documentation

- [Deploy with Docker Compose or systemd](docs/deployment.md)
- [Configure local and production email](docs/email.md)
- [Extend the boilerplate](docs/extending.md)
- [Review the boilerplate roadmap](docs/roadmap.md)

## Stack

- Python 3.14
- Django 6.0
- PostgreSQL 18
- uv
- Docker Compose
- Gunicorn and Nginx
