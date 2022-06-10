from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from project.utils import admin as admin_utils

from .forms import DepartmentAdminForm, FacultyAdminForm, UniversityAdminForm
from .models import Department, Faculty, University


@admin.register(University)
class UniversityAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the University model."""

    class FacultyInline(admin.TabularInline):
        model = Faculty
        extra = 0

    form = UniversityAdminForm

    model_accusative = _("uczelnię")
    model_genitive_plural = _("uczelni")

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
class FacultyAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the Faculty model."""

    class DepartmentInline(admin.TabularInline):
        model = Department
        extra = 0

    form = FacultyAdminForm

    model_accusative = _("wydział")
    model_genitive_plural = _("wydziałów")

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Pola podstawowe"), {"fields": ("name", "code")}),
        (_("Jednostka nadrzędna"), {"fields": ("university",)}),
    )
    readonly_fields = ("id",)
    autocomplete_fields = ("university",)
    inlines = (DepartmentInline,)

    list_display = (
        "id",
        "name",
        "code",
        admin_utils.related_object_link(University),
        "departments",
    )
    list_filter = ("university",)
    search_fields = (
        "name",
        "code",
        "university__name",
        "university__code",
    )

    @admin.display(description=Department._meta.verbose_name_plural.capitalize())
    def departments(self, obj):
        links = admin_utils.related_objects_links(
            obj,
            related_model="department",
            content_field="name",
        )
        if links:
            return format_html("<br>".join(links))


@admin.register(Department)
class DepartmentAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the Department model."""

    form = DepartmentAdminForm

    model_accusative = _("katedrę")
    model_genitive_plural = _("katedr")

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Pola podstawowe"), {"fields": ("name", "code")}),
        (_("Jednostka nadrzędna"), {"fields": ("faculty",)}),
    )
    readonly_fields = ("id",)
    autocomplete_fields = ("faculty",)

    list_display = (
        "id",
        "name",
        "code",
        admin_utils.related_object_link(Faculty, content_field="name"),
        admin_utils.related_object_link(University, content_field="name"),
    )
    list_filter = (
        admin_utils.RelatedModelFilter.as_filter(
            model=Faculty,
            lookup="faculty",
            field="name",
        ),
        admin_utils.RelatedModelFilter.as_filter(
            model=University,
            lookup="faculty__university",
            field="name",
        ),
    )
    search_fields = (
        "name",
        "code",
        "faculty__name",
        "faculty__code",
        "faculty__university__name",
        "faculty__university__code",
    )
