from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

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
        "last_name",
        "is_staff",
        "has_employee",
    )
    list_display_links = ("id",)
    ordering = ("id",)
