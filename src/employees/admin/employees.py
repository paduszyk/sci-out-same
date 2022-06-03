from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from authorships.models import Author
from units.models import Department

from ..forms import DegreeAdminForm, EmployeeAdminForm, StatusAdminForm
from ..models import Degree, Discipline, Employee, Employment, Status


class EmploymentInline(admin.TabularInline):
    """A class to represent the employment inline form."""

    model = Employment
    extra = 0


class AuthorInline(admin.TabularInline):
    """A class to represent the author inline form."""

    model = Author
    extra = 0


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    """Admin options for the Status model."""

    form = StatusAdminForm

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Dane podstawowe"), {"fields": ("name", "abbr")}),
    )
    readonly_fields = ("id",)

    list_display = ("id", "name", "abbr")
    search_fields = ("name", "abbr")


@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    """Admin options for the Degree model."""

    form = DegreeAdminForm

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Dane podstawowe"), {"fields": ("abbr",)}),
    )
    readonly_fields = ("id",)

    list_display = ("id", "abbr")
    search_fields = ("abbr",)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Admin options for the Employee model."""

    form = EmployeeAdminForm

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Identyfikatory"), {"fields": ("user", "slug")}),
        (_("Dane naukowe"), {"fields": ("degree", "orcid")}),
        (_("Ewaluacja"), {"fields": ("in_evaluation", "discipline")}),
        (_("Dane dodatkowe"), {"fields": ("status",)}),
    )
    readonly_fields = ("id",)
    inlines = (EmploymentInline, AuthorInline)

    list_display = (
        "id",
        "last_name",
        "first_name",
        "degree",
        "status_abbr",
        "in_evaluation",
        "discipline_abbr",
        "is_employed",
        "department_abbr",
    )
    search_fields = ("id", "user__last_name", "user__first_name")

    @admin.display(
        description=Status._meta.verbose_name.capitalize(),
        ordering="status__abbr",
    )
    def status_abbr(self, obj):
        """Return abbreviation of employee's status."""
        return obj.status.abbr

    @admin.display(
        description=Discipline._meta.verbose_name.capitalize(),
        ordering="discipline__abbr",
    )
    def discipline_abbr(self, obj):
        """Return abbreviation of employee's discipline."""
        if obj.discipline:
            return obj.discipline.abbr

    @admin.display(
        description=Department._meta.verbose_name.capitalize(),
        ordering="employment__department__abbr",
    )
    def department_abbr(self, obj):
        """Return abbreviation of employee's department."""
        if obj.is_employed():
            return obj.employment.department.abbr
