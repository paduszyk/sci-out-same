from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from project.utils import admin as admin_utils

from ..contributions.models import ArticleContribution
from .forms import ArticleAdminForm, JournalAdminForm, PublisherAdminForm
from .models import Article, Journal, Publisher


@admin.register(Publisher)
class PublisherAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the Publisher model."""

    form = PublisherAdminForm

    model_accusative = _("wydawnictwo")
    model_genitive_plural = _("wydawnictw")

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Pola podstawowe"), {"fields": ("name", "abbreviation")}),
        (_("Dane dodatkowe"), {"fields": ("international",)}),
    )
    readonly_fields = ("id",)

    list_display = ("id", "name", "abbreviation", "international")
    list_filter = ("international",)
    search_fields = ("name", "abbreviation")


class JournalByAncestorFilter(admin.SimpleListFilter):
    """A class to represent filter of Journal objects by ancestor existence."""

    title = _("Ma poprzednika")
    parameter_name = "has_ancestor"

    def lookups(obj, request, model_admin):
        return [("True", _("Tak")), ("False", _("Nie"))]

    def queryset(obj, request, queryset):
        if obj.value():
            return queryset.filter(ancestor__isnull=obj.value() != "True")


@admin.register(Journal)
class JournalAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the Journal model."""

    form = JournalAdminForm

    model_accusative = _("czasopismo")
    model_genitive_plural = _("czasopism")

    fieldsets = (
        (None, {"fields": ("id",)}),
        (
            _("Pola podstawowe"),
            {
                "fields": (
                    "publisher",
                    "title",
                    "abbreviation",
                    "issn",
                )
            },
        ),
        (_("Ewaluacja"), {"fields": ("impact_factor", "points")}),
        (_("Pola dodatkowe"), {"fields": ("ancestor",)}),
    )
    readonly_fields = ("id",)

    list_display = (
        "id",
        "title",
        "abbreviation",
        admin_utils.related_object_link(Publisher, content_field="abbreviation"),
        "issn",
        "impact_factor",
        "points",
        admin_utils.related_object_link(
            Journal,
            fk_field="ancestor",
            description=_("Poprzednik"),
            content_field="abbreviation",
        ),
    )
    list_filter = (
        admin_utils.RelatedModelFilter.as_filter(
            model=Publisher,
            lookup="publisher",
            field="name",
            null=True,
        ),
        JournalByAncestorFilter,
    )
    search_fields = (
        "title",
        "abbreviation",
        "issn",
        "ancestor__title",
        "ancestor__abbreviation",
        "ancestor__issn",
        "ancestor__publisher__name",
        "ancestor__publisher__abbreviation",
        "publisher__name",
        "publisher__abbreviation",
    )


@admin.register(Article)
class ArticleAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the Article model."""

    class ArticleContributionInline(admin.TabularInline):
        model = ArticleContribution
        extra = 0

    form = ArticleAdminForm

    model_accusative = _("artykuł")
    model_genitive_plural = _("artykułów")

    fieldsets = (
        (None, {"fields": ("id",)}),
        (
            _("Pola podstawowe"),
            {
                "fields": (
                    "title",
                    "journal",
                    "year",
                    ("volume", "issue"),
                    ("first_page", "last_page"),
                )
            },
        ),
        (_("Ewaluacja"), {"fields": ("impact_factor", "points")}),
        (_("Pola dodatkowe"), {"fields": ("doi", "url")}),
        (_("Administracja"), {"fields": ("locked",)}),
    )
    readonly_fields = ("id", "impact_factor", "points")
    autocomplete_fields = ("journal",)
    inlines = (ArticleContributionInline,)

    list_display = (
        "id",
        "get_contribution_links",
        "title",
        admin_utils.related_object_link(Journal, content_field="abbreviation"),
        "year",
        "locked",
    )
    list_filter = ("year", "locked")
    search_fields = (
        "title",
        "journal__title",
        "journal__abbreviation",
        "journal__publisher__name",
        "journal__publisher__abbreviation",
    )
