# Quick Start

This path runs Django on the host with live reload while PostgreSQL, Redis, Mailpit, and Adminer run in containers.

## Requirements

- Python 3.14
- `mise` or another Python version manager
- `uv`
- Docker Engine with Docker Compose v2

## Start the Project

```sh
cp .env.example .env
mise install
uv sync --group cache
docker compose -f compose.yaml -f compose.local.yaml up -d db redis mailpit adminer
uv run python manage.py migrate
uv run python manage.py runserver
```

Open <http://127.0.0.1:8000/>.

Local services:

| Service | Address | Purpose |
| --- | --- | --- |
| Django | <http://127.0.0.1:8000/> | Application development server |
| PostgreSQL | `127.0.0.1:5432` | Application database |
| Redis | `127.0.0.1:6379` | Shared cache |
| Mailpit | <http://localhost:8025> | Captured development email |
| Adminer | <http://localhost:8080> | Database browser |

## Create an Administrator

```sh
uv run python manage.py createsuperuser
```

## Run Checks

```sh
make test
make check
```

## Next Step

Follow [Extending the Boilerplate](Extending-the-Boilerplate) to build and test a complete Django module.
