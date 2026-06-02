from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        # import signal handlers to ensure they're registered
        try:
            import core.signals  # noqa: F401
        except Exception:
            # avoid breaking startup if signals have issues; they will be logged
            import logging

            logging.getLogger(__name__).exception('Failed to import core.signals')
