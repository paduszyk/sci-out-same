from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .forms import AuthorAdminForm, AuthorshipAdminForm
from .models import Author, Authorship


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


@admin.register(Authorship)
class AuthorshipAdmin(admin.ModelAdmin):
    """Admin options for the Authorship model."""

    form = AuthorshipAdminForm

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Dane podstawowe"), {"fields": ("author",)}),
        (_("Dane dodatkowe"), {"fields": ("order",)}),
        (_("Obiekt"), {"fields": ("content_type", "object_id")}),
    )
    readonly_fields = ("id",)

    list_display = (
        "id",
        "content_type_name",
        "object_id",
        "order",
        "get_alias",
        "by_employee",
    )
    search_fields = ("author__alias",)

    @admin.display(description=_("Typ obiektu"))
    def content_type_name(self, obj):
        """Return 'name' field of the ContentType object."""
        return obj.content_type.name
