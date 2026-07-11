# Deployment

This setup runs Django with Gunicorn, serves static files through WhiteNoise, and stores application data in PostgreSQL.

Choose Docker Compose or a native host deployment.

## Compose Files

- `compose.yaml` defines shared Django and PostgreSQL services.
- `compose.local.yaml` adds self-signed HTTPS on local port 8000.
- `compose.prod.yaml` adds domain-based Nginx on public ports 80 and 443.

Always combine the shared file with exactly one environment-specific file.

## Local Production Simulation

This mode runs the production image, Gunicorn, PostgreSQL, Nginx, HTTPS redirects, and Django production security settings.
It does not require Nginx or OpenSSL on the host.

Ensure `.env` trusts both local HTTPS origins:

```dotenv
CSRF_TRUSTED_ORIGINS=https://localhost:8000,https://127.0.0.1:8000
```

Start the stack:

```sh
docker compose -f compose.yaml -f compose.local.yaml up --build -d
```

Open `https://localhost:8000` and accept the self-signed certificate warning.
Nginx terminates TLS and proxies requests to Gunicorn without requiring Nginx or OpenSSL on the host.

View logs or stop the local stack:

```sh
docker compose -f compose.yaml -f compose.local.yaml logs -f nginx web
docker compose -f compose.yaml -f compose.local.yaml down
```

## Docker Compose Production

### Requirements

- Docker Engine
- Docker Compose v2
- A server with public ports 80 and 443
- A domain whose DNS records point to the server
- A trusted TLS certificate for that domain

### Configure

Create the production environment file:

```sh
cp .env.example .env
```

Set these values before deployment:

```dotenv
DEBUG=False
SECRET_KEY=<generate-a-long-random-value>
DOMAIN=example.com
TLS_CERT_DIR=/etc/learn-django/certs
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

Place the trusted certificate files from your certificate provider in `TLS_CERT_DIR` on the server:

```text
/etc/learn-django/certs/fullchain.pem
/etc/learn-django/certs/privkey.pem
```

Certificate files are ignored by Git.
Renew them through the certificate provider or deployment platform before they expire.

### Start

Build and start the services:

```sh
docker compose -f compose.yaml -f compose.prod.yaml up --build -d
```

Compose waits for PostgreSQL, applies migrations, starts Gunicorn on internal port 8001, and exposes Nginx on ports 80 and 443.

Verify HTTPS and application readiness:

```sh
curl --fail https://example.com/health/
```

Create an administrator:

```sh
docker compose -f compose.yaml -f compose.prod.yaml exec web .venv/bin/python manage.py createsuperuser
```

Run Django's production checks:

```sh
docker compose -f compose.yaml -f compose.prod.yaml exec web .venv/bin/python manage.py check --deploy
```

### HTTPS

The production override terminates TLS in Nginx and forwards the original `Host` and HTTPS scheme to Django.
Only ports 80 and 443 are published.
Gunicorn and PostgreSQL remain private inside the Compose network.

### Update

Pull the new code and recreate the web service:

```sh
git pull
docker compose -f compose.yaml -f compose.prod.yaml up --build -d
```

Migrations run automatically before Gunicorn starts.

### Operations

View logs:

```sh
docker compose -f compose.yaml -f compose.prod.yaml logs -f nginx web
```

Stop services without deleting data:

```sh
docker compose -f compose.yaml -f compose.prod.yaml down
```

Back up PostgreSQL:

```sh
docker compose -f compose.yaml -f compose.prod.yaml exec -T db sh -c 'pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB"' > backup.sql
```

Named volumes retain PostgreSQL and local uploaded media.
Back up both volumes, or use `STORAGE_PROVIDER=s3` for durable uploaded media.

## Native Host

Use this option when Docker and Docker Compose are unavailable or unwanted.

### Requirements

- Python 3.14
- `uv`
- PostgreSQL
- systemd or another process supervisor
- A server with ports 80 and 443 available for a reverse proxy

Create a dedicated operating-system user and clone the repository into a stable location such as `/srv/learn-django`.
The examples below use user `learn-django` and that directory.

### Configure PostgreSQL

Create a PostgreSQL database and role using your provider's control panel or PostgreSQL administration tools.
Do not run Django with a PostgreSQL superuser.

Copy and configure the environment file:

```sh
cp .env.example .env
```

Use production values and point Django at the PostgreSQL host:

```dotenv
DEBUG=False
SECRET_KEY=<generate-a-long-random-value>
ALLOWED_HOSTS=example.com,www.example.com
CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com
POSTGRES_DB_NAME=learn_django
POSTGRES_USER=learn_django
POSTGRES_PASSWORD=<generate-a-long-random-value>
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
STORAGE_PROVIDER=local
```

Set `POSTGRES_HOST` to the provider hostname when PostgreSQL runs on another server.
Keep `.env` readable only by the application user and never commit it.

### Install and Prepare

Install locked production dependencies:

```sh
uv sync --frozen --no-dev --group prod
```

Apply migrations, collect static files, and run deployment checks:

```sh
uv run python manage.py migrate
uv run python manage.py collectstatic --noinput
uv run python manage.py check --deploy
```

Create an administrator:

```sh
uv run python manage.py createsuperuser
```

Do not use Django's development server in production.

### Run with systemd

Create `/etc/systemd/system/learn-django.service`:

```ini
[Unit]
Description=Learn Django Gunicorn service
After=network.target postgresql.service

[Service]
Type=simple
User=learn-django
Group=learn-django
WorkingDirectory=/srv/learn-django
ExecStart=/srv/learn-django/.venv/bin/gunicorn --config gunicorn.conf.py app.wsgi:application --bind 127.0.0.1:8000
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

If PostgreSQL is remote, remove `postgresql.service` from `After`.
Enable and start the service:

```sh
sudo systemctl daemon-reload
sudo systemctl enable --now learn-django
sudo systemctl status learn-django
```

Verify application and database readiness:

```sh
curl --fail http://127.0.0.1:8000/health/
```

### HTTPS

Place Caddy, Nginx, or another TLS-terminating reverse proxy in front of `127.0.0.1:8000`.
Forward the original `Host` and `X-Forwarded-Proto` headers.
Keep Gunicorn bound to localhost so it is not exposed publicly.

### Update

Pull code, synchronize dependencies, apply migrations, collect static files, then restart Gunicorn:

```sh
git pull
uv sync --frozen --no-dev --group prod
uv run python manage.py migrate
uv run python manage.py collectstatic --noinput
uv run python manage.py check --deploy
sudo systemctl restart learn-django
curl --fail http://127.0.0.1:8000/health/
```

### Operations

View logs:

```sh
sudo journalctl -u learn-django -f
```

Back up PostgreSQL:

```sh
pg_dump --host="$POSTGRES_HOST" --username="$POSTGRES_USER" "$POSTGRES_DB_NAME" > backup.sql
```

Back up the `media/` directory when `STORAGE_PROVIDER=local`.
When `STORAGE_PROVIDER=s3`, configure AWS S3 or an S3-compatible service such as Cloudflare R2 in `.env` and include the bucket in the backup policy.
