from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ArticlesConfig(AppConfig):
    """A class to represent the articles app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "articles"
    verbose_name = _("artykuły")

    def ready(self):
        """Run the following code when Django starts."""
        from . import signals
