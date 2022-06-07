from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from project.utils import related_model_count as count

from ..forms import DisciplineAdminForm, DomainAdminForm
from ..models import Discipline, Domain, Employee


class DisciplineInline(admin.TabularInline):
    """A class to represent the Discipline model inline form."""

    model = Discipline
    extra = 0


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    """A class to represent admin options for the Domain model."""

    form = DomainAdminForm

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Dane podstawowe"), {"fields": ("name",)}),
    )
    readonly_fields = ("id",)
    inlines = (DisciplineInline,)

    list_display = ("id", "name", count(Discipline), count(Employee))
    search_fields = ("name",)


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    """A class to represent admin options for the Discipline model."""

    form = DisciplineAdminForm

    fieldsets = (
        (None, {"fields": ("id",)}),
        (_("Dane podstawowe"), {"fields": ("name", "abbr")}),
        (_("Klasyfikacja"), {"fields": ("domain",)}),
    )
    readonly_fields = ("id",)

    list_display = ("id", "name", "abbr", "domain", count(Employee))
    search_fields = ("name", "abbr", "domain__name")
