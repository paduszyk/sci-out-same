from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EmployeesConfig(AppConfig):
    """A class to represent the app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "employees"
    verbose_name = _("Kadra")
