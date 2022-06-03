from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuthorshipsConfig(AppConfig):
    """A class to represent the authorships app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "authorships"
    verbose_name = _("autorstwa")
