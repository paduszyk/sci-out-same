from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from employees.models import Employee
from project.utils import related_model_count as count

from .forms import DepartmentAdminForm, FacultyAdminForm, UniversityAdminForm
from .models import Department, Faculty, University


class FacultyInline(admin.TabularInline):
    """A class to represent the Faculty model inline form."""

    model = Faculty
    extra = 0


class DepartmentInline(admin.TabularInline):
    """A class to represent the Department model inline form."""

    model = Department
    extra = 0


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    """A class to represent admin options for the University model."""

    form = UniversityAdminForm

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Dane podstawowe"), {"fields": ("name", "abbr")}),
    )
    readonly_fields = ("id",)
    inlines = (FacultyInline,)

    list_display = (
        "id",
        "name",
        "abbr",
        count(Faculty),
        count(Department),
        count(Employee),
    )
    search_fields = ("name", "abbr")


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    """A class to represent admin options for the Faculty model."""

    form = FacultyAdminForm

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Dane podstawowe"), {"fields": ("name", "abbr")}),
        (_("Jednostka nadrzędna"), {"fields": ("university",)}),
    )
    readonly_fields = ("id",)
    inlines = (DepartmentInline,)

    list_display = (
        "id",
        "name",
        "abbr",
        "university",
        count(Department),
        count(Employee),
    )
    search_fields = ("name", "abbr", "university__name", "university__abbr")


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """A class to represent admin options for the Department model."""

    form = DepartmentAdminForm

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Dane podstawowe"), {"fields": ("name", "abbr")}),
        (_("Jednostka nadrzędna"), {"fields": ("faculty",)}),
    )
    readonly_fields = ("id",)

    list_display = (
        "id",
        "name",
        "abbr",
        "faculty",
        "university",
        count(Employee),
    )
    search_fields = (
        "name",
        "abbr",
        "faculty__name",
        "faculty__abbr",
        "faculty__university__name",
        "faculty__university__abbr",
    )
