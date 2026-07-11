# Email

Django uses its built-in SMTP backend for local and production email delivery.
No provider-specific package is required.

## Local Mailpit

Start the local production simulation:

```sh
docker compose -f compose.yaml -f compose.local.yaml up --build -d
```

Mailpit accepts SMTP on port 1025 and provides its inbox at <http://localhost:8025>.
Messages are captured locally and are not delivered to real recipients.

Send a test message through Django:

```sh
docker compose -f compose.yaml -f compose.local.yaml exec web .venv/bin/python manage.py sendtestemail you@example.com
```

Open Mailpit and confirm the message appears.

## Production SMTP Provider

Use any provider that exposes SMTP credentials, including Amazon SES, Mailgun, Postmark, Resend, or SendGrid.

Configure `.env` using values supplied by the provider:

```dotenv
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=<smtp-username>
EMAIL_HOST_PASSWORD=<smtp-password>
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
DEFAULT_FROM_EMAIL="Example <noreply@example.com>"
```

Use `EMAIL_USE_TLS=True` for explicit TLS, commonly on port 587.
Use `EMAIL_USE_SSL=True` for implicit TLS, commonly on port 465.
Never enable both settings.
Keep SMTP credentials only in the production secret store or private `.env` file.

After deployment, verify delivery:

```sh
docker compose -f compose.yaml -f compose.prod.yaml exec web .venv/bin/python manage.py sendtestemail you@example.com
```

Configure SPF, DKIM, and DMARC records through the provider before sending production mail.

## New User Password Setup

Creating a user with an email address automatically sends a one-time password setup link after the database transaction commits.
Set `SITE_URL` to the public application origin so generated links use the correct domain:

```dotenv
SITE_URL=https://example.com
```

For `make run`, use `SITE_URL=http://127.0.0.1:8000`.
The local Compose override sets its own HTTPS URL automatically.

Users without an email address are created without sending a message.
Passwords are never included in email.
