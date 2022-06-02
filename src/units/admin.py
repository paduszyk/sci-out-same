from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .forms import DepartmentAdminForm, FacultyAdminForm, UniversityAdminForm
from .models import Department, Faculty, University


class FacultyInline(admin.TabularInline):
    """A class to represent the faculty inline form."""

    model = Faculty
    extra = 0


class DepartmentInline(admin.TabularInline):
    """A class to represent the department inline form."""

    model = Department
    extra = 0


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    """Admin options for the University model."""

    form = UniversityAdminForm

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Dane podstawowe"), {"fields": ("name", "abbr")}),
    )
    readonly_fields = ("id",)
    inlines = [FacultyInline]

    list_display = ("id", "name", "abbr", "get_faculty_count", "get_department_count")
    search_fields = ("name", "abbr")


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    """Admin options for the Faculty model."""

    form = FacultyAdminForm

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Dane podstawowe"), {"fields": ("name", "abbr")}),
        (_("Jednostka nadrzędna"), {"fields": ("university",)}),
    )
    readonly_fields = ("id",)
    inlines = [DepartmentInline]

    list_display = ("id", "name", "abbr", "university", "get_department_count")
    search_fields = ("name", "abbr", "university__name", "university__abbr")


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Admin options for the Department model."""

    form = DepartmentAdminForm

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Dane podstawowe"), {"fields": ("name", "abbr")}),
        (_("Jednostka nadrzędna"), {"fields": ("faculty",)}),
    )
    readonly_fields = ("id",)

    list_display = ("id", "name", "abbr", "faculty", "get_university")
    search_fields = (
        "name",
        "abbr",
        "faculty__name",
        "faculty__abbr",
        "faculty__university__name",
        "faculty__university__abbr",
    )

    @admin.display(description=University._meta.verbose_name.capitalize())
    def get_university(self, obj):
        """Return university of the department object's faculty."""
        return obj.faculty.university
