# Extend the Boilerplate

Feature code lives under `modules/`.
Each Django module uses packages instead of growing large `models.py`, `views.py`, `admin.py`, or `tests.py` files.

This tutorial adds a complete `blog` module.

## 1. Create the Module

Run:

```sh
make create-app NAME=blog
```

The command creates:

```text
modules/blog/
├── admin/
│   └── __init__.py
├── migrations/
│   └── __init__.py
├── models/
│   └── __init__.py
├── tests/
│   └── __init__.py
├── views/
│   └── __init__.py
├── __init__.py
└── apps.py
```

The generated `AppConfig.name` is `modules.blog`.

## 2. Register the Module

Add the module before `django_cleanup.apps.CleanupConfig` in `app/settings.py`:

```python
INSTALLED_APPS = [
    # Existing apps...
    "modules.blog",
    "django_cleanup.apps.CleanupConfig",
]
```

Keep `django_cleanup.apps.CleanupConfig` last so its signal handlers run after other apps.

## 3. Add a Model

Create `modules/blog/models/post.py`:

```python
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

Export every model from `modules/blog/models/__init__.py` so Django discovers it:

```python
from modules.blog.models.post import Post
```

Create and apply migrations:

```sh
uv run python manage.py makemigrations blog
uv run python manage.py migrate
```

Commit generated migrations.
Never edit migrations already applied in shared or production environments.

## 4. Add Admin Management

Create `modules/blog/admin/post.py`:

```python
from django.contrib import admin
from unfold.admin import ModelAdmin

from modules.blog.models.post import Post


@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ("title", "published", "created_at")
    list_filter = ("published",)
    search_fields = ("title", "body")
    readonly_fields = ("created_at",)
```

Import each admin module from `modules/blog/admin/__init__.py` so Django admin autodiscovery loads it:

```python
from modules.blog.admin.post import PostAdmin
```

## 5. Add a View

Create `modules/blog/views/post.py`:

```python
from django.shortcuts import render

from modules.blog.models.post import Post


def post_list(request):
    posts = Post.objects.filter(published=True).order_by("-created_at")
    return render(request, "blog/post_list.html", {"posts": posts})
```

Export the view from `modules/blog/views/__init__.py`:

```python
from modules.blog.views.post import post_list
```

## 6. Add URLs

Create `modules/blog/urls.py`:

```python
from django.urls import path

from modules.blog.views import post_list

app_name = "blog"

urlpatterns = [
    path("", post_list, name="post-list"),
]
```

Include it from `app/urls.py`:

```python
urlpatterns = [
    path("blog/", include("modules.blog.urls")),
    path("", admin.site.urls),
]
```

Keep feature URLs before the root admin route because Django admin has a final catch-all view.

## 7. Add a Template

Create `modules/blog/templates/blog/post_list.html`:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Blog</title>
  </head>
  <body>
    <main>
      <h1>Blog</h1>
      {% for post in posts %}
        <article>
          <h2>{{ post.title }}</h2>
          <p>{{ post.body }}</p>
        </article>
      {% empty %}
        <p>No published posts.</p>
      {% endfor %}
    </main>
  </body>
</html>
```

## 8. Add Tests

Create `modules/blog/tests/test_post_list.py`:

```python
from django.test import TestCase
from django.urls import reverse

from modules.blog.models.post import Post


class PostListTests(TestCase):
    def test_shows_only_published_posts(self):
        Post.objects.create(title="Visible", body="Published", published=True)
        Post.objects.create(title="Hidden", body="Draft", published=False)

        response = self.client.get(reverse("blog:post-list"))

        self.assertContains(response, "Visible")
        self.assertNotContains(response, "Hidden")
```

Test modules do not need exports in `tests/__init__.py`.

Run:

```sh
make test
make check
```

## 9. Grow Packages Safely

Use one file per cohesive concept, not automatically one file per class.

Example:

```text
modules/blog/
├── admin/
│   ├── __init__.py
│   ├── category.py
│   └── post.py
├── models/
│   ├── __init__.py
│   ├── category.py
│   └── post.py
├── tests/
│   ├── __init__.py
│   ├── test_category.py
│   └── test_post.py
└── views/
    ├── __init__.py
    ├── category.py
    └── post.py
```

Explicitly export models, admin registrations, and public views from their package `__init__.py` files.
Avoid empty `services/`, `selectors/`, or `repositories/` packages until feature code needs those boundaries.

## 10. Deploy

Build and recreate services:

```sh
docker compose up --build -d
```

Container startup applies committed migrations and collects static files before Gunicorn starts.

Verify the release:

```sh
docker compose exec web .venv/bin/python manage.py check --deploy
docker compose logs web
```

See [deployment.md](deployment.md) for HTTPS, updates, and backups.

## Feature Checklist

- Module lives under `modules/`.
- Module is registered before `django_cleanup.apps.CleanupConfig`.
- Models are exported from `models/__init__.py`.
- Admin modules are imported from `admin/__init__.py`.
- Model changes include generated migrations.
- Feature URLs are included by `app/urls.py`.
- User-visible behavior has tests under `tests/`.
- New environment variables are documented in `.env.example`.
- `make test` and `make check` pass.
