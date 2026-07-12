import os
import subprocess
import sys

from django.test import SimpleTestCase


class BackendSettingsTests(SimpleTestCase):
    def run_settings(self, **environment):
        process_environment = os.environ.copy()
        process_environment.update(environment)
        return subprocess.run(
            [
                sys.executable,
                "-c",
                "from django.conf import settings; "
                "print(settings.CACHES['default']['BACKEND']); "
                "print(settings.EMAIL_BACKEND)",
            ],
            capture_output=True,
            env=process_environment,
            text=True,
        )

    def test_supported_backends_are_selected(self):
        result = self.run_settings(CACHE_BACKEND="locmem", EMAIL_BACKEND="console")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout.splitlines(),
            [
                "django.core.cache.backends.locmem.LocMemCache",
                "django.core.mail.backends.console.EmailBackend",
            ],
        )

    def test_redis_requires_url(self):
        result = self.run_settings(CACHE_BACKEND="redis", CACHE_URL="")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("CACHE_URL is required", result.stderr)

    def test_unknown_backend_is_rejected(self):
        result = self.run_settings(CACHE_BACKEND="unknown")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unsupported CACHE_BACKEND", result.stderr)

    def test_smtp_rejects_tls_and_ssl_together(self):
        result = self.run_settings(
            EMAIL_BACKEND="smtp", EMAIL_USE_TLS="True", EMAIL_USE_SSL="True"
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("cannot both be enabled", result.stderr)
