from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from project.utils import admin as admin_utils

from .forms import DepartmentAdminForm, FacultyAdminForm, UniversityAdminForm
from .models import Department, Faculty, University


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    """A class to represent admin options for the University model."""

    class FacultyInline(admin.TabularInline):
        model = Faculty
        extra = 0

    form = UniversityAdminForm

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Pola podstawowe"), {"fields": ("name", "code")}),
    )
    readonly_fields = ("id",)
    inlines = (FacultyInline,)

    list_display = ("id", "name", "code", "faculties")
    search_fields = ("name", "code")

    @admin.display(description=Faculty._meta.verbose_name_plural.capitalize())
    def faculties(self, obj):
        links = admin_utils.related_objects_links(
            obj,
            related_model="faculty",
            content_field="name",
        )
        if links:
            return format_html("<br>".join(links))


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    """A class to represent admin options for the Faculty model."""

    class DepartmentInline(admin.TabularInline):
        model = Department
        extra = 0

    form = FacultyAdminForm

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Pola podstawowe"), {"fields": ("name", "code")}),
        (_("Jednostka nadrzędna"), {"fields": ("university",)}),
    )
    readonly_fields = ("id",)
    inlines = (DepartmentInline,)

    list_display = ("id", "name", "code", "university__name", "departments")
    list_filter = ("university",)
    search_fields = (
        "name",
        "code",
        "university__name",
        "university__code",
    )

    @admin.display(
        description=University._meta.verbose_name,
        ordering="university__name",
    )
    def university__name(self, obj):
        return obj.university.name

    @admin.display(description=Department._meta.verbose_name_plural.capitalize())
    def departments(self, obj):
        links = admin_utils.related_objects_links(
            obj,
            related_model="department",
            content_field="name",
        )
        if links:
            return format_html("<br>".join(links))


class DepartmentByFacultyFilter(admin.SimpleListFilter):
    """Admin list filter of the Department objects by the related Faculty objects."""

    title = Faculty._meta.verbose_name
    parameter_name = Faculty._meta.model_name

    def lookups(self, request, model_admin):
        return ((faculty.id, faculty.name) for faculty in Faculty.objects.all())

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(faculty__id__exact=self.value())


class DepartmentByUniversityFilter(admin.SimpleListFilter):
    """Admin list filter of the Department objects by the related University objects."""

    title = University._meta.verbose_name
    parameter_name = Department._meta.model_name

    def lookups(self, request, model_admin):
        return (
            (university.id, university.name) for university in University.objects.all()
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(faculty__university__id__exact=self.value())


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """A class to represent admin options for the Department model."""

    form = DepartmentAdminForm

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Pola podstawowe"), {"fields": ("name", "code")}),
        (_("Jednostka nadrzędna"), {"fields": ("faculty",)}),
    )
    readonly_fields = ("id",)

    list_display = ("id", "name", "code", "faculty__name", "university__name")
    list_filter = (
        DepartmentByFacultyFilter,
        DepartmentByUniversityFilter,
    )
    search_fields = (
        "name",
        "code",
        "faculty__name",
        "faculty__code",
        "faculty__university__name",
        "faculty__university__code",
    )

    @admin.display(
        description=Faculty._meta.verbose_name,
        ordering="faculty__name",
    )
    def faculty__name(self, obj):
        return obj.faculty.name

    @admin.display(
        description=University._meta.verbose_name,
        ordering="faculty__university__name",
    )
    def university__name(self, obj):
        return obj.university.name
