from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from ..forms import (
    EmploymentAdminForm,
    GroupAdminForm,
    PositionAdminForm,
    SubgroupAdminForm,
)
from ..models import Employment, Group, Position, Subgroup


class SubgroupInline(admin.TabularInline):
    """A class to represent the subgroup inline form."""

    model = Subgroup
    extra = 0


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Admin options for the Group model."""

    form = GroupAdminForm

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Dane podstawowe"), {"fields": ("name", "abbr")}),
    )
    readonly_fields = ("id",)
    inlines = (SubgroupInline,)

    list_display = (
        "id",
        "name",
        "abbr",
        "get_subgroup_count",
        "get_position_count",
        "get_employee_count",
    )
    search_fields = ("name", "abbr")


@admin.register(Subgroup)
class SubgroupAdmin(admin.ModelAdmin):
    """Admin options for the Subgroup model."""

    form = SubgroupAdminForm

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Dane podstawowe"), {"fields": ("name", "abbr")}),
        (_("Klasyfikacja"), {"fields": ("group",)}),
    )
    readonly_fields = ("id",)

    list_display = (
        "id",
        "name",
        "abbr",
        "group",
        "get_position_count",
        "get_employee_count",
    )
    search_fields = ("name", "abbr", "group__name", "group__abbr")


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    """Admin options for the Position model."""

    form = PositionAdminForm

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Dane podstawowe"), {"fields": ("name",)}),
        (_("Klasyfikacja"), {"fields": ("subgroups",)}),
    )
    readonly_fields = ("id",)

    list_display = (
        "id",
        "name",
        "group_list",
        "subgroup_list",
        "is_classified",
        "get_employee_count",
    )
    search_fields = (
        "name",
        "subgroups__name",
        "subgroups__abbr",
        "subgroups__group__name",
        "subgroups__group__abbr",
    )

    @admin.display(description=Group._meta.verbose_name_plural.capitalize())
    def group_list(self, obj):
        """Return positions's groups."""
        return format_html(
            "<br>".join(obj.get_groups().values_list("name", flat=True)),
        )

    @admin.display(description=Subgroup._meta.verbose_name_plural.capitalize())
    def subgroup_list(self, obj):
        """Return position's subgroups."""
        return format_html(
            "<br>".join(obj.subgroups.all().values_list("name", flat=True)),
        )


@admin.register(Employment)
class EmploymentAdmin(admin.ModelAdmin):
    """Admin options for the Employment model."""

    form = EmploymentAdminForm

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Klasyfikacja"), {"fields": ("position", "subgroup")}),
        (_("Jednostka"), {"fields": ("department",)}),
    )
    readonly_fields = ("id",)

    list_display = (
        "id",
        "position",
        "subgroup",
        "department",
    )
    search_fields = (
        "position__name",
        "position__subgroups__name",
        "position__subgroups__abbr",
        "position__subgroups__group__name",
        "position__subgroups__group__abbr",
        "department__name",
        "department__abbr",
        "subgroup__name",
        "subgroup__abbr",
    )
