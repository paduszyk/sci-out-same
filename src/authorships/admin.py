from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from project.utils import related_model_count as count

from .forms import AuthorAdminForm, AuthorshipAdminForm, AuthorshipTypeAdminForm
from .models import Author, Authorship, AuthorshipType


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Admin options for the Author model."""

    form = AuthorAdminForm

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Dane podstawowe"), {"fields": ("employee", "alias")}),
    )
    readonly_fields = ("id",)

    list_display = (
        "id",
        "employee",
        "alias",
        count(Authorship),
    )
    search_fields = (
        "alias",
        "employee__user__username",
        "employee__user__last_name",
        "employee__user__first_name",
    )


@admin.register(AuthorshipType)
class AuthorshipTypeAdmin(admin.ModelAdmin):
    """Admin options for the AuthorshipType model."""

    form = AuthorshipTypeAdminForm

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Dane podstawowe"), {"fields": ("name", "abbr")}),
    )
    readonly_fields = ("id",)

    list_display = ("id", "name", "abbr", count(Authorship))
    search_fields = ("name", "abbr")


@admin.register(Authorship)
class AuthorshipAdmin(admin.ModelAdmin):
    """Admin options for the Authorship model."""

    form = AuthorshipAdminForm

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Dane podstawowe"), {"fields": ("author", "type", "department")}),
        (_("Dane dodatkowe"), {"fields": ("order", "contribution", "corresponding")}),
        (_("Obiekt"), {"fields": ("content_type", "object_id")}),
    )
    readonly_fields = ("id",)
    autocomplete_fields = ("author",)

    list_display = (
        "id",
        "content_type__name",
        "object_id",
        "order",
        "alias",
        "type__abbr",
        "department__abbr",
    )
    search_fields = ("author__alias", "type__name", "type__abbr")

    @admin.display(description=_("Typ obiektu"))
    def content_type__name(self, obj):
        return obj.content_type.name

    @admin.display(description=_("Typ"), ordering="type__abbr")
    def type__abbr(self, obj):
        if obj.type:
            return obj.type.abbr

    @admin.display(description=_("Katedra"))
    def department__abbr(self, obj):
        if obj.department:
            return obj.department.abbr
