# learn-django

Small Django learning project.

## Stack

- Python 3.14
- Django 6.0
- SQLite for local development
- uv for dependency management
- mise for local Python version pinning

## Setup

Install Python 3.14 with your preferred tool, or use mise:

```sh
mise install
```

Install dependencies:

```sh
uv sync
```

Apply database migrations:

```sh
uv run python manage.py migrate
```

Run the development server:

```sh
uv run python manage.py runserver
```

Open <http://127.0.0.1:8000/>.

Admin lives at <http://127.0.0.1:8000/admin/>.

Create an admin user when needed:

```sh
uv run python manage.py createsuperuser
```

## Makefile

Common commands are available through `make`:

```sh
make install          # Install dependencies
make migrate          # Apply migrations
make run              # Run Django development server
make test             # Run Django tests
make check            # Run Django system checks
make deploy-check     # Run Django deployment checks
make superuser        # Create admin user
```

Override the development server port with `PORT`:

```sh
make run PORT=8080
```

## Project Layout

```text
app/             Django project package
app/settings.py  Django settings
app/urls.py      Root URL configuration
modules/         Feature modules
manage.py        Django management entrypoint
pyproject.toml   Project metadata and dependencies
uv.lock          Locked dependency versions
```

## Notes

This project uses Django's default local settings: `DEBUG=True`,
SQLite, and a development secret key.

Do not use these settings directly for production.

## Documentation

- [Deploy with Docker Compose](docs/deployment.md)
- [Extend the boilerplate](docs/extending.md)
- [Boilerplate roadmap](docs/roadmap.md)
