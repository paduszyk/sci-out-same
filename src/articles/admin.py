from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.translation import gettext_lazy as _

from authorships.models import Authorship
from project.utils import related_model_count as count

from .forms import ArticleAdminForm, JournalAdminForm
from .models import Article, Journal


class AuthorshipInline(GenericTabularInline):
    """A class to represent the Authorship model inline form."""

    model = Authorship
    extra = 0
    autocomplete_fields = ("author",)


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    """A class to represent admin options for the Journal model."""

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
        "ancestor__title",
        "successors__title",
        count(Article),
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
    def ancestor__title(self, obj):
        if obj.ancestor:
            return obj.ancestor.title

    @admin.display(description=_("Następcy"))
    def successors__title(self, obj):
        if obj.successors:
            return ", ".join(obj.successors.all().values_list("title", flat=True))


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """A class to represent admin options for the Article model."""

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
    autocomplete_fields = ("journal",)
    inlines = (AuthorshipInline,)

    list_display = (
        "id",
        "author_count",
        "authors",
        "title",
        "journal__abbr",
        "year",
        "locked",
    )
    search_fields = (
        "title",
        "journal__title",
        "journal__abbr",
        "year",
    )
    actions = ("lock", "unlock")

    @admin.display(
        description=Journal._meta.verbose_name.capitalize(),
        ordering="journal__abbr",
    )
    def journal__abbr(self, obj):
        return obj.journal.abbr

    @admin.action(description=_("Zablokuj wybrane artykuły"))
    def lock(self, request, queryset):
        queryset.update(locked=True)

    @admin.action(description=_("Odblokuj wybrane artykuły"))
    def unlock(self, request, queryset):
        queryset.update(locked=False)
