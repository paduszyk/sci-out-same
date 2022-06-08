from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from project.utils import admin as admin_utils

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


@admin.register(Degree)
class DegreeAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the Degree model."""

    form = DegreeAdminForm

    model_accusative = _("tytuł/stopień naukowy")
    model_genitive_plural = _("tytułów/stopni naukowych")


@admin.register(Domain)
class DomainAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the Domain model."""

    form = DomainAdminForm

    model_accusative = _("dziedzinę nauki")
    model_genitive_plural = _("dziedzin nauki")


@admin.register(Discipline)
class DisciplineAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the Discipline model."""

    form = DisciplineAdminForm

    model_accusative = _("dyscyplinę nauki")
    model_genitive_plural = _("dyscyplin nauki")


@admin.register(Group)
class GroupAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the Group model."""

    form = GroupAdminForm

    model_accusative = _("grupę")
    model_genitive_plural = _("grup")


@admin.register(Subgroup)
class SubgroupAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the Subgroup model."""

    form = SubgroupAdminForm

    model_accusative = _("podgrupę")
    model_genitive_plural = _("podgrup")


@admin.register(Position)
class PositionAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the Position model."""

    form = PositionAdminForm

    model_accusative = _("stanowisko")
    model_genitive_plural = _("stanowisk")


@admin.register(Employee)
class EmployeeAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the Employee model."""

    form = EmployeeAdminForm

    model_accusative = _("pracownika")
    model_genitive_plural = _("pracowników")


@admin.register(Employment)
class EmploymentAdmin(admin_utils.ModelAdmin):
    """A class to represent admin options for the Employment model."""

    form = EmploymentAdminForm

    model_accusative = _("zatrudnienie")
    model_genitive_plural = _("zatrudnień")
