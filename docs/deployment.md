# Deploy with Docker Compose

This setup runs Django with Gunicorn, serves static files through WhiteNoise, and stores application data in PostgreSQL.

## Requirements

- Docker Engine
- Docker Compose v2
- A server with ports 80 and 443 available for a reverse proxy

## Configure

Create the production environment file:

```sh
cp .env.example .env
```

Set these values before deployment:

```dotenv
DEBUG=False
SECRET_KEY=<generate-a-long-random-value>
ALLOWED_HOSTS=example.com,www.example.com
CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com
POSTGRES_DB_NAME=learn_django
POSTGRES_USER=learn_django
POSTGRES_PASSWORD=<generate-a-long-random-value>
POSTGRES_HOST=db
POSTGRES_PORT=5432
STORAGE_PROVIDER=local
```

Keep `.env` private and never commit it.

## Start

Build and start the services:

```sh
docker compose up --build -d
```

Compose waits for PostgreSQL, applies migrations, then starts Gunicorn on port 8000.

Create an administrator:

```sh
docker compose exec web .venv/bin/python manage.py createsuperuser
```

Run Django's production checks:

```sh
docker compose exec web .venv/bin/python manage.py check --deploy
```

## HTTPS

Place Caddy, Nginx, or another TLS-terminating reverse proxy in front of port 8000.
Forward the original `Host` header and `X-Forwarded-Proto` header.
Do not expose port 8000 publicly after the proxy is configured.

## Update

Pull the new code and recreate the web service:

```sh
git pull
docker compose up --build -d
```

Migrations run automatically before Gunicorn starts.

## Operations

View logs:

```sh
docker compose logs -f web
```

Stop services without deleting data:

```sh
docker compose down
```

Back up PostgreSQL:

```sh
docker compose exec -T db pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB_NAME" > backup.sql
```

Named volumes retain PostgreSQL and local uploaded media.
Back up both volumes, or use `STORAGE_PROVIDER=s3` for durable uploaded media.
