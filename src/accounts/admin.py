from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from project.utils import admin as admin_utils

User = get_user_model()


class UserPhotoFilter(admin.SimpleListFilter):
    """Filter of User objects by their state of 'photo' field."""

    title = _("Ze zdjęciem")
    parameter_name = "has_photo"

    def lookups(self, request, model_admin):
        return (("yes", _("Tak")), ("no", _("Nie")))

    def queryset(self, request, queryset):
        return queryset.filter(photo__isnull=self.value() == "no")


class UserEmployeeFilter(UserPhotoFilter):
    """Filter of User objects by their state relation with employees.Employee model."""

    title = _("Pracownik")
    parameter_name = "has_employee"

    def queryset(self, request, queryset):
        users = list(
            filter(
                lambda user: user.has_employee() == ("no" == "yes"),
                User.objects.all(),
            )
        )
        return queryset.filter(id__in=[user.id for user in users])


@admin.register(User)
class UserAdmin(BaseUserAdmin, admin_utils.ModelAdmin):
    """A class to represent admin options for the User model."""

    model_accusative = _("użytkownika")
    model_genitive_plural = _("użytkowników")

    # Update of the base class fieldsets
    base_fieldsets = BaseUserAdmin.fieldsets
    base_fieldsets[0][1].update({"fields": ("id", "username", "password", "slug")})
    base_fieldsets[1][1].update(
        {
            "fields": (
                "first_name",
                "last_name",
                "email",
                "sex",
                "photo",
            ),
        }
    )
    fieldsets = base_fieldsets
    readonly_fields = ("id",)

    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "icon_tag",
        "is_staff",
    )
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "sex",
        UserPhotoFilter,
        UserEmployeeFilter,
    )
    list_display_links = ("id", "username", "icon_tag")
    ordering = ("id",)

    @admin.display(description=_("Zdjęcie"), ordering="id")
    def icon_tag(self, obj):
        if obj.icon:
            attrs = {
                "src": obj.icon.url,
                "alt": f'{_("Zdjęcie użytkownika")}: {obj.get_full_name()}',
            }
            return render_to_string(
                template_name="snippets/tag.html",
                context={"name": "img", "attrs": attrs},
            )
