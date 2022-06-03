from django.contrib import admin
from django.utils.translation import gettext_lazy as _

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
        "get_authorship_count",
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

    list_display = ("id", "name", "abbr", "get_authorship_count")
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

    list_display = (
        "id",
        "content_type_name",
        "object_id",
        "order",
        "get_alias",
        "type_abbr",
        "by_employee",
        "department_abbr",
    )
    search_fields = ("author__alias", "type__name", "type__abbr")

    @admin.display(description=_("Typ obiektu"))
    def content_type_name(self, obj):
        """Return 'name' field of the ContentType object."""
        return obj.content_type.name

    @admin.display(description=_("Typ"), ordering="type__abbr")
    def type_abbr(self, obj):
        """Return abbreviation of the authorship type related to the object."""
        if obj.type:
            return obj.type.abbr

    @admin.display(description=_("Katedra"))
    def department_abbr(self, obj):
        """Return abbreviation of the department related to the object."""
        if obj.department:
            return obj.department.abbr
