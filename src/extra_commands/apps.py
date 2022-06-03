from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ExtraCommandsConfig(AppConfig):
    """A class to represent the extra_commands app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "extra_commands"
    verbose_name = _("dodatkowe polecenia")
