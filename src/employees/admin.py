from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from project.utils import admin as admin_utils
from units.models import Department

from .forms import (
    DegreeAdminForm,
    DisciplineAdminForm,
    DomainAdminForm,
    EmployeeAdminForm,
    EmploymentAdminForm,
    GroupAdminForm,
    PositionAdminForm,
    StatusAdminForm,
    SubgroupAdminForm,
)
from .models import (
    Degree,
    Discipline,
    Domain,
    Employee,
    Employment,
    Group,
    Position,
    Status,
    Subgroup,
)


@admin.register(Status)
class StatusAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the Status model."""

    form = StatusAdminForm

    model_accusative = _("status")
    model_genitive_plural = _("statusów")

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Pola podstawowe"), {"fields": ("name", "code")}),
    )
    readonly_fields = ("id",)

    list_display = ("id", "name", "code")
    search_fields = ("name", "code")


@admin.register(Degree)
class DegreeAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the Degree model."""

    form = DegreeAdminForm

    model_accusative = _("tytuł/stopień naukowy")
    model_genitive_plural = _("tytułów/stopni naukowych")

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Pola podstawowe"), {"fields": ("code",)}),
    )
    readonly_fields = ("id",)

    list_display = ("id", "code")
    search_fields = ("code",)


class DisciplineInline(admin.TabularInline):
    """A class to represent inline form for the Discipline model."""

    model = Discipline
    extra = 0


@admin.register(Domain)
class DomainAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the Domain model."""

    form = DomainAdminForm

    model_accusative = _("dziedzinę nauki")
    model_genitive_plural = _("dziedzin nauki")

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Pola podstawowe"), {"fields": ("name", "code")}),
    )
    readonly_fields = ("id",)
    inlines = (DisciplineInline,)

    list_display = ("id", "name", "code", "disciplines")
    search_fields = ("name", "code")

    @admin.display(description=Discipline._meta.verbose_name_plural.capitalize())
    def disciplines(self, obj):
        links = admin_utils.related_objects_links(
            obj,
            related_model="discipline",
            content_field="name",
        )
        if links:
            return format_html("<br>".join(links))


@admin.register(Discipline)
class DisciplineAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the Discipline model."""

    form = DisciplineAdminForm

    model_accusative = _("dyscyplinę nauki")
    model_genitive_plural = _("dyscyplin nauki")

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Pola podstawowe"), {"fields": ("name", "code")}),
        (_("Klasyfikacja"), {"fields": ("domain",)}),
    )
    readonly_fields = ("id",)
    autocomplete_fields = ("domain",)

    list_display = ("id", "name", "code", "domain")
    list_filter = ("domain",)
    search_fields = ("name", "code", "domain__name", "domain__code")


class SubgroupInline(admin.TabularInline):
    """A class to represent inline form for the Subgroup model."""

    model = Subgroup
    extra = 0


@admin.register(Group)
class GroupAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the Group model."""

    form = GroupAdminForm

    model_accusative = _("grupę")
    model_genitive_plural = _("grup")

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Pola podstawowe"), {"fields": ("name", "code")}),
    )
    readonly_fields = ("id",)
    inlines = (SubgroupInline,)

    list_display = ("id", "name", "code", "subgroups")
    search_fields = ("name", "code")

    @admin.display(description=Subgroup._meta.verbose_name_plural.capitalize())
    def subgroups(self, obj):
        links = admin_utils.related_objects_links(
            obj,
            related_model="subgroup",
            content_field="name",
        )
        if links:
            return format_html("<br>".join(links))


@admin.register(Subgroup)
class SubgroupAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the Subgroup model."""

    form = SubgroupAdminForm

    model_accusative = _("podgrupę")
    model_genitive_plural = _("podgrup")

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Pola podstawowe"), {"fields": ("name", "code")}),
        (_("Klasyfikacja"), {"fields": ("group",)}),
    )
    readonly_fields = ("id",)
    autocomplete_fields = ("group",)

    list_display = ("id", "name", "code", "group")
    list_filter = ("group",)
    search_fields = ("name", "code", "group__name", "group__code")


@admin.register(Position)
class PositionAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the Position model."""

    form = PositionAdminForm

    model_accusative = _("stanowisko")
    model_genitive_plural = _("stanowisk")

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Pola podstawowe"), {"fields": ("name",)}),
        (_("Klasyfikacja"), {"fields": ("subgroup_set",)}),
    )
    readonly_fields = ("id",)
    autocomplete_fields = ("subgroup_set",)

    list_display = ("id", "name", "group", "subgroups")
    list_filter = (
        admin_utils.RelatedModelFilter.as_filter(
            model=Group,
            lookup="subgroup_set__group",
            field="name",
        ),
        admin_utils.RelatedModelFilter.as_filter(
            model=Subgroup,
            lookup="subgroup_set",
            field="name",
        ),
    )
    search_fields = ("name", "subgroup_set__name", "subgroup_set__code")

    @admin.display(description=Subgroup._meta.verbose_name_plural.capitalize())
    def subgroups(self, obj):
        links = admin_utils.related_objects_links(
            obj,
            related_model="subgroup",
            content_field="name",
        )
        if links:
            return format_html("<br>".join(links))


class EmploymentInline(admin.StackedInline):
    """A class to represent inline form for the Employment model."""

    model = Employment
    form = EmploymentAdminForm

    extra = 0

    fieldsets = (
        (_("Stanowisko"), {"fields": ("subgroup", "position")}),
        (_("Jednostka"), {"fields": ("department",)}),
    )
    autocomplete_fields = ("subgroup", "position", "department")


@admin.register(Employee)
class EmployeeAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the Employee model."""

    form = EmployeeAdminForm

    model_accusative = _("pracownika")
    model_genitive_plural = _("pracowników")

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Pola podstawowe"), {"fields": ("user", "status")}),
        (_("Dane naukowe"), {"fields": ("degree", "orcid")}),
        (_("Ewaluacja"), {"fields": ("in_evaluation", "discipline")}),
    )
    readonly_fields = ("id",)
    autocomplete_fields = ("user", "status", "degree", "discipline")
    inlines = (EmploymentInline,)

    list_display = (
        "id",
        "last_name",
        "first_name",
        "degree",
        "status__code",
        "positions__name",
        "groups__code",
        "subgroups__code",
        "departments__code",
        "in_evaluation",
    )
    list_display_links = ()
    list_filter = (
        "status",
        "degree",
        "in_evaluation",
        admin_utils.RelatedModelFilter.as_filter(
            model=Group,
            lookup="employment__subgroup__group",
            field="name",
            null=True,
        ),
        admin_utils.RelatedModelFilter.as_filter(
            model=Subgroup,
            lookup="employment__subgroup",
            field="name",
            null=True,
        ),
        admin_utils.RelatedModelFilter.as_filter(
            model=Position,
            lookup="employment__subgroup__position",
            field="name",
            null=True,
        ),
        admin_utils.RelatedModelFilter.as_filter(
            model=Department,
            lookup="employment__department",
            field="get_full_code",
            null=True,
        ),
    )
    list_editable = ("in_evaluation",)
    search_fields = (
        "user__username",
        "user__last_name",
        "user__first_name",
        "orcid",
    )

    @admin.display(
        description=Status._meta.verbose_name.capitalize(),
        ordering="status__code",
    )
    def status__code(self, obj):
        if obj.status:
            return obj.status.code

    @admin.display(
        description=Position._meta.verbose_name.capitalize(),
        ordering="employment__position__name",
    )
    def positions__name(self, obj):
        return format_html(
            "<br>".join(
                [position.name if position else "-" for position in obj.positions]
            )
        )

    @admin.display(
        description=Group._meta.verbose_name.capitalize(),
        ordering="employment__group__code",
    )
    def groups__code(self, obj):
        return format_html(
            "<br>".join(
                [subgroup.group.code if subgroup else "-" for subgroup in obj.subgroups]
            )
        )

    @admin.display(
        description=Subgroup._meta.verbose_name.capitalize(),
        ordering="employment__subgroup__code",
    )
    def subgroups__code(self, obj):
        return format_html(
            "<br>".join(
                [subgroup.code if subgroup else "-" for subgroup in obj.subgroups]
            )
        )

    @admin.display(
        description=Department._meta.verbose_name.capitalize(),
        ordering="employment__department__code",
    )
    def departments__code(self, obj):
        return format_html(
            "<br>".join(
                [
                    department.get_full_code() if department else "-"
                    for department in obj.departments
                ]
            )
        )


@admin.register(Employment)
class EmploymentAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the Employment model."""

    form = EmploymentAdminForm

    model_accusative = _("zatrudnienie")
    model_genitive_plural = _("zatrudnień")

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Pola podstawowe"), {"fields": ("employee",)}),
        (_("Stanowisko"), {"fields": ("subgroup", "position")}),
        (_("Jednostka"), {"fields": ("department",)}),
    )
    readonly_fields = ("id",)
    autocomplete_fields = ("employee", "subgroup", "position", "department")

    list_display = (
        "id",
        "employee",
        "group__code",
        "subgroup__code",
        "position",
        "department__code",
    )
    list_filter = (
        admin_utils.RelatedModelFilter.as_filter(
            model=Group,
            lookup="subgroup__group",
            field="name",
            null=True,
        ),
        "subgroup",
        "position",
        admin_utils.RelatedModelFilter.as_filter(
            model=Department,
            lookup="department",
            field="get_full_code",
            null=True,
        ),
    )
    search_fields = (
        "employee__user__last_name",
        "employee__user__first_name",
        "position__name",
        "subgroup__name",
        "subgroup__code",
        "subgroup__group__name",
        "subgroup__group__code",
    )

    @admin.display(
        description=Group._meta.verbose_name.capitalize(),
        ordering="subgroup__group__code",
    )
    def group__code(self, obj):
        if obj.subgroup:
            return obj.subgroup.group.code

    @admin.display(
        description=Subgroup._meta.verbose_name.capitalize(),
        ordering="subgroup__code",
    )
    def subgroup__code(self, obj):
        if obj.subgroup:
            return obj.subgroup.code

    @admin.display(
        description=Department._meta.verbose_name.capitalize(),
        ordering="department__code",
    )
    def department__code(self, obj):
        if obj.department:
            return obj.department.get_full_code()
