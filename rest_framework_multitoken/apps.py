from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MultiTokenConfig(AppConfig):
    name = "rest_framework_multitoken"
    verbose_name = _("Multi Token")
