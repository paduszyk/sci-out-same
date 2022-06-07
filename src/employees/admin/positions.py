from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from project.utils import related_model_count as count
from units.models import Department

from ..forms import (
    EmploymentAdminForm,
    GroupAdminForm,
    PositionAdminForm,
    SubgroupAdminForm,
)
from ..models import Employee, Employment, Group, Position, Subgroup


class SubgroupInline(admin.TabularInline):
    """A class to represent the Subgroup model inline form."""

    model = Subgroup
    extra = 0


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """A class to represent admin options for the Group model."""

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
        count(Subgroup),
        count(Position),
        count(Employee),
    )
    search_fields = ("name", "abbr")


@admin.register(Subgroup)
class SubgroupAdmin(admin.ModelAdmin):
    """A class to represent admin options for the Subgroup model."""

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
        count(Position),
        count(Employee),
    )
    search_fields = ("name", "abbr", "group__name", "group__abbr")


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    """A class to represent admin options for the Position model."""

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
        count(Employee),
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
        return format_html(
            "<br>".join(obj.get_groups().values_list("name", flat=True)),
        )

    @admin.display(description=Subgroup._meta.verbose_name_plural.capitalize())
    def subgroup_list(self, obj):
        return format_html(
            "<br>".join(obj.subgroups.all().values_list("name", flat=True)),
        )


@admin.register(Employment)
class EmploymentAdmin(admin.ModelAdmin):
    """A class to represent admin options for the Employment model."""

    form = EmploymentAdminForm

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Klasyfikacja"), {"fields": ("position", "subgroup")}),
        (_("Jednostka"), {"fields": ("department",)}),
    )
    readonly_fields = ("id",)

    list_display = (
        "id",
        "employee",
        "position",
        "group__abbr",
        "subgroup__abbr",
        "department__abbr",
    )
    search_fields = (
        "employee__user__last_name",
        "employee__user__first_name",
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

    @admin.display(
        description=Group._meta.verbose_name.capitalize(),
        ordering="subgroup__group__abbr",
    )
    def group__abbr(self, obj):
        return obj.subgroup.group.abbr

    @admin.display(
        description=Subgroup._meta.verbose_name.capitalize(),
        ordering="subgroup__group",
    )
    def subgroup__abbr(self, obj):
        return obj.subgroup.abbr

    @admin.display(
        description=Department._meta.verbose_name.capitalize(),
        ordering="department__abbr",
    )
    def department__abbr(self, obj):
        return obj.department.abbr
