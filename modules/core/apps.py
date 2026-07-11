from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "modules.core"

    def ready(self):
        import modules.core.signals  # noqa: F401
