from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from project.utils import admin as admin_utils

from .forms import ArticleAdminForm, JournalAdminForm, PublisherAdminForm
from .models import Article, Journal, Publisher


@admin.register(Publisher)
class PublisherAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the Publisher model."""

    form = PublisherAdminForm

    model_accusative = _("wydawnictwo")
    model_genitive_plural = _("wydawnictw")


@admin.register(Journal)
class JournalAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the Journal model."""

    form = JournalAdminForm

    model_accusative = _("czasopismo")
    model_genitive_plural = _("czasopism")


@admin.register(Article)
class ArticleAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the Article model."""

    form = ArticleAdminForm

    model_accusative = _("artykuł")
    model_genitive_plural = _("artykułów")
