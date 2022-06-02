from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UnitsConfig(AppConfig):
    """A class to represent the units app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "units"
    verbose_name = _("jednostki")
