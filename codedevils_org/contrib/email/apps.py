from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EmailConfig(AppConfig):
    name = "codedevils_org.contrib.email"
    verbose_name = _("Email")

    def ready(self):
        try:
            import codedevils_org.contrib.email.signals  # noqa F401
        except ImportError:
            pass
