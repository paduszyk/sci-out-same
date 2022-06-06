from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin options for the User model."""

    # Update of the base class fieldsets
    base_fieldsets = BaseUserAdmin.fieldsets
    base_fieldsets[0][1].update({"fields": ("id", "username", "password")})
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
        "get_user_icon",
        "last_name",
        "is_staff",
        "has_employee",
    )
    list_display_links = ("id",)
    ordering = ("id",)

    @admin.display(description=_("Zdjęcie"))
    def get_user_icon(self, obj):
        """Return HTML of the user's photo."""
        if obj.icon:
            attrs = {
                "src": obj.icon.url,
                "alt": f'{_("Zdjęcie użytkownika")}: {obj.get_full_name()}',
            }
            return render_to_string(
                template_name="snippets/tag.html",
                context={"name": "img", "attrs": attrs},
            )
