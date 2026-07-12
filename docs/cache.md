# Cache

Django's cache API is always available, while `CACHE_BACKEND` selects its implementation.
Application code should use `django.core.cache.cache` and should not inspect the selected backend.

## Disabled Cache

Caching is disabled by default:

```dotenv
CACHE_BACKEND=dummy
```

The dummy backend accepts cache operations but never stores values.
Application correctness must not depend on cached data.

## Local Memory

Use local memory for development or a single-process deployment:

```dotenv
CACHE_BACKEND=locmem
```

Each process has a separate cache.
Do not use this mode when workers need shared values.

## Redis

The local Compose stack starts Redis, exposes it on port 6379, and configures the web service to use it.

Install the optional cache dependency:

```sh
uv sync --group cache
```

Configure Redis running on the host:

```dotenv
CACHE_BACKEND=redis
CACHE_URL=redis://127.0.0.1:6379/1
```

For a Redis service named `redis` on a Compose network, use:

```dotenv
CACHE_URL=redis://redis:6379/1
```

The application fails during startup when Redis mode has no URL.
Redis connection failures do not silently fall back to process-local memory.
