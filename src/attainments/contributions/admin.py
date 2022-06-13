from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from project.utils import admin as admin_utils

from .forms import (
    ArticleContributionAdminForm,
    AuthorAdminForm,
    ContributionStatusAdminForm,
)
from .models import ArticleContribution, Author, ContributionStatus


class AuthorByEmployeeFilter(admin.SimpleListFilter):
    """A class to represent filter of Author objects by employee existence."""

    title = _("Ma pracownika")
    parameter_name = "has_employee"

    def lookups(obj, request, model_admin):
        return [("True", _("Tak")), ("False", _("Nie"))]

    def queryset(obj, request, queryset):
        if obj.value():
            return queryset.filter(employee__isnull=obj.value() != "True")


@admin.register(Author)
class AuthorAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the Author model."""

    form = AuthorAdminForm

    model_accusative = _("autora")
    model_genitive_plural = _("autorów")

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Pola podstawowe"), {"fields": ("alias", "employee")}),
    )
    readonly_fields = ("id",)
    autocomplete_fields = ("employee",)

    list_display = (
        "id",
        "alias",
        admin_utils.related_object_link("employees.Employee"),
    )
    list_filter = (AuthorByEmployeeFilter,)
    search_fields = (
        "alias",
        "employee__user__last_name",
        "employee__user__first_name",
    )


@admin.register(ContributionStatus)
class ContributionStatusAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the ContributionStatus model."""

    form = ContributionStatusAdminForm

    model_accusative = _("status")
    model_genitive_plural = _("statusów")

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Pola podstawowe"), {"fields": ("name", "code")}),
    )
    readonly_fields = ("id",)

    list_display = ("id", "name", "code")
    search_fields = ("name", "code")


@admin.register(ArticleContribution)
class ArticleContributionAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the ArticleContribution model."""

    form = ArticleContributionAdminForm

    model_accusative = _("udział")
    model_genitive_plural = _("udziałów")

    def has_add_permission(self, request, obj=None):
        return False
