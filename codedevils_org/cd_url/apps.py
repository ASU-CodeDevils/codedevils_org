from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CDUrlConfig(AppConfig):
    name = "codedevils_org.cd_url"
    verbose_name = _("CodeDevils URLs")
