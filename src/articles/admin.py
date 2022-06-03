from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .forms import ArticleAdminForm, JournalAdminForm
from .models import Article, Journal


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    """Admin options for the Journal model."""

    form = JournalAdminForm

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Dane podstawowe"), {"fields": ("title", "abbr")}),
        (_("Ewaluacja"), {"fields": ("impact_factor", "points")}),
        (_("Dane dodatkowe"), {"fields": ("ancestor",)}),
    )
    readonly_fields = ("id",)

    list_display = (
        "id",
        "title",
        "abbr",
        "impact_factor",
        "points",
        "ancestor_title",
        "successors_titles",
        "get_article_count",
    )
    search_fields = (
        "title",
        "abbr",
        "ancestor__title",
        "ancestor__abbr",
        "successors__title",
        "successors__abbr",
    )

    @admin.display(description=_("Przodek"), ordering="ancestor__title")
    def ancestor_title(self, obj):
        """Return journal's ancestor title."""
        if obj.ancestor:
            return obj.ancestor.title

    @admin.display(description=_("Następcy"))
    def successors_titles(self, obj):
        """Return journal's successors titles."""
        if obj.successors:
            return ", ".join(obj.successors.all().values_list("title", flat=True))


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Admin options for Article model."""

    form = ArticleAdminForm

    fieldsets = (
        (None, {"fields": ("id",)}),
        (
            _("Dane podstawowe"),
            {
                "fields": ("title", "journal", "year", "volume", "pages"),
            },
        ),
        (_("Dane dodatkowe"), {"fields": ("doi",)}),
        (_("Ewaluacja"), {"fields": ("impact_factor", "points", "locked")}),
    )
    readonly_fields = ("id", "impact_factor", "points")

    list_display = ("id", "title", "journal_abbr", "year", "locked")
    search_fields = (
        "title",
        "journal__title",
        "journal__abbr",
        "year",
    )
    actions = ("lock_articles", "unlock_articles")

    @admin.display(
        description=Journal._meta.verbose_name.capitalize(),
        ordering="journal__abbr",
    )
    def journal_abbr(self, obj):
        """Get the article's journal abbreviation."""
        return obj.journal.abbr

    @admin.action(description=_("Zablokuj wybrane artykuły"))
    def lock_articles(self, request, queryset):
        """Lock the articles from the queryset."""
        queryset.update(locked=True)

    @admin.action(description=_("Odblokuj wybrane artykuły"))
    def unlock_articles(self, request, queryset):
        """Unlock the articles from the queryset."""
        queryset.update(locked=False)
