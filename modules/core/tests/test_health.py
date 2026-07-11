from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.db import DatabaseError
from django.test import TestCase
from django.urls import reverse

from modules.samples.models import Book


class StarterTests(TestCase):
    def test_root_redirects_to_admin_login(self):
        response = self.client.get("/", secure=True)

        self.assertRedirects(
            response, "/login/?next=/", fetch_redirect_response=False
        )

    def test_admin_login_is_available(self):
        response = self.client.get("/login/", secure=True)

        self.assertEqual(response.status_code, 200)

    def test_admin_add_user_form_has_required_fields(self):
        admin = get_user_model().objects.create_superuser(
            username="admin", password="admin-password"
        )
        self.client.force_login(admin)

        response = self.client.get(reverse("admin:auth_user_add"), secure=True)

        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, "Create password now?")

    def test_health_reports_ready(self):
        response = self.client.get(reverse("health"), secure=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    @patch("modules.core.views.connection.ensure_connection", side_effect=DatabaseError)
    def test_health_reports_database_failure(self, ensure_connection):
        response = self.client.get(reverse("health"), secure=True)

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {"status": "unavailable"})

    def test_book_can_be_created(self):
        book = Book.objects.create(name="Django", published_date="2026-07-11")

        self.assertEqual(Book.objects.get(pk=book.pk).slug, "django")
