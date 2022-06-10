from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AttainmentsConfig(AppConfig):
    """A class to represent the app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "attainments"
    verbose_name = _("Dorobek")
