from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from authorships.models import Author, Authorship
from project.utils import related_model_count as count
from units.models import Department

from ..forms import DegreeAdminForm, EmployeeAdminForm, StatusAdminForm
from ..models import Degree, Discipline, Employee, Employment, Status


class EmploymentInline(admin.TabularInline):
    """A class to represent the Employment model inline form."""

    model = Employment
    extra = 0


class AuthorInline(admin.TabularInline):
    """A class to represent the Author model inline form."""

    model = Author
    extra = 0


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    """A class to represent admin options for the Status model."""

    form = StatusAdminForm

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Dane podstawowe"), {"fields": ("name", "abbr")}),
    )
    readonly_fields = ("id",)

    list_display = ("id", "name", "abbr", count(Employee))
    search_fields = ("name", "abbr")


@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    """A class to represent admin options for the Degree model."""

    form = DegreeAdminForm

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Dane podstawowe"), {"fields": ("abbr",)}),
    )
    readonly_fields = ("id",)

    list_display = ("id", "abbr", count(Employee))
    search_fields = ("abbr",)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """A class to represent admin options for the Employee model."""

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
        "status__abbr",
        "in_evaluation",
        "discipline__abbr",
        "is_employed",
        "department__abbr",
        count(Authorship),
    )
    search_fields = ("id", "user__last_name", "user__first_name")

    @admin.display(
        description=Status._meta.verbose_name.capitalize(),
        ordering="status__abbr",
    )
    def status__abbr(self, obj):
        return obj.status.abbr

    @admin.display(
        description=Discipline._meta.verbose_name.capitalize(),
        ordering="discipline__abbr",
    )
    def discipline__abbr(self, obj):
        if obj.discipline:
            return obj.discipline.abbr

    @admin.display(
        description=Department._meta.verbose_name.capitalize(),
        ordering="employment__department__abbr",
    )
    def department__abbr(self, obj):
        if obj.is_employed():
            return obj.employment.department.abbr
