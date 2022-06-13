from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from project.utils import admin as admin_utils

from .forms import (
    ArticleContributionAdminForm,
    AuthorAdminForm,
    ContributionStatusAdminForm,
)
from .models import ArticleContribution, Author, ContributionStatus


@admin.register(Author)
class AuthorAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the Author model."""

    form = AuthorAdminForm

    model_accusative = _("autora")
    model_genitive_plural = _("autorów")


@admin.register(ContributionStatus)
class ContributionStatusAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the ContributionStatus model."""

    form = ContributionStatusAdminForm

    model_accusative = _("status")
    model_genitive_plural = _("statusów")


@admin.register(ArticleContribution)
class ArticleContributionAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the ArticleContribution model."""

    form = ArticleContributionAdminForm

    model_accusative = _("udział")
    model_genitive_plural = _("udziałów")

    def has_add_permission(self, request, obj=None):
        return False
