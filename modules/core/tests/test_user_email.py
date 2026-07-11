from urllib.parse import urlparse

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    SITE_URL="https://example.com",
)
class UserEmailTests(TestCase):
    def setUp(self):
        admin = get_user_model().objects.create_superuser(
            username="admin", password="admin-password"
        )
        self.client.force_login(admin)

    def test_new_user_can_set_password_from_email(self):
        with self.captureOnCommitCallbacks(execute=True):
            user = get_user_model().objects.create_user(
                username="new-user", email="new@example.com"
            )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Welcome - set up your account")
        self.assertEqual(mail.outbox[0].alternatives[0].mimetype, "text/html")
        setup_url = next(
            line for line in mail.outbox[0].body.splitlines() if line.startswith("https://")
        )

        response = self.client.get(urlparse(setup_url).path, secure=True)
        response = self.client.post(
            response.url,
            {"new_password1": "A-secure-password-123", "new_password2": "A-secure-password-123"},
            secure=True,
        )

        user.refresh_from_db()
        self.assertRedirects(
            response, "/accounts/reset/done/", fetch_redirect_response=False
        )
        self.assertTrue(user.check_password("A-secure-password-123"))

    def test_admin_created_user_receives_valid_setup_link(self):
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(
                reverse("admin:auth_user_add"),
                {
                    "username": "admin-created",
                    "email": "admin-created@example.com",
                    "usable_password": "false",
                    "password1": "",
                    "password2": "",
                    "_save": "Save",
                },
                secure=True,
            )

        self.assertEqual(response.status_code, 302)
        setup_url = next(
            line for line in mail.outbox[0].body.splitlines() if line.startswith("https://")
        )
        response = self.client.get(urlparse(setup_url).path, secure=True)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/set-password/", response.url)
