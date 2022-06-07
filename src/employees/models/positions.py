from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _

from units.models import Department

from .employees import Employee


class Group(models.Model):
    """A class to represent the Group objects."""

    name = models.CharField(_("nazwa"), max_length=255)
    abbr = models.CharField(_("skrót"), max_length=255)

    class Meta:
        verbose_name = _("grupa pracowników")
        verbose_name_plural = _("grupy pracowników")
        ordering = ("id",)

    class Manager(models.Manager):
        def get_queryset(self):
            """Update the queryset by some annotations."""
            return (
                super()
                .get_queryset()
                .annotate(
                    subgroup_count=models.Count(
                        "subgroups",
                        distinct=True,
                    ),
                    position_count=models.Count(
                        "subgroups__position",
                        distinct=True,
                    ),
                    employee_count=models.Count(
                        "subgroups__employments__employee",
                        distinct=True,
                    ),
                )
            )

    objects = Manager()

    def __str__(self):
        return f"{self.name} ({self.abbr})"


class Subgroup(models.Model):
    """A class to represent the Subgroup objects."""

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name=Group._meta.verbose_name,
        related_name="subgroups",
    )
    name = models.CharField(_("nazwa"), max_length=255)
    abbr = models.CharField(_("skrót"), max_length=255)

    class Meta:
        verbose_name = _("podgrupa pracowników")
        verbose_name_plural = _("podgrupy pracowników")
        ordering = ("id",)

    class Manager(models.Manager):
        def get_queryset(self):
            """Update the queryset by some annotations."""
            return (
                super()
                .get_queryset()
                .annotate(
                    position_count=models.Count(
                        "position",
                        distinct=True,
                    ),
                    employee_count=models.Count(
                        "employments__employee",
                        distinct=True,
                    ),
                )
            )

    objects = Manager()

    def __str__(self):
        return f"{self.name} ({self.group.name})"


class Position(models.Model):
    """A class to represent the Position objects."""

    name = models.CharField(_("nazwa"), max_length=255)
    subgroups = models.ManyToManyField(
        Subgroup,
        verbose_name=Subgroup._meta.verbose_name_plural,
    )

    class Meta:
        verbose_name = _("stanowisko")
        verbose_name_plural = _("stanowiska")
        ordering = ("id",)

    class Manager(models.Manager):
        def get_queryset(self):
            """Update the queryset by some annotations."""
            return (
                super()
                .get_queryset()
                .annotate(
                    employee_count=models.Count(
                        "employments__employee",
                        distinct=True,
                    ),
                )
            )

    objects = Manager()

    def __str__(self):
        return self.name

    def get_groups(self):
        """Return the position's groups based on its subgroups."""
        if self.subgroups.exists():
            return Group.objects.filter(
                id__in=[subgroup.group.id for subgroup in self.subgroups.all()]
            )
        return Group.objects.none()

    @admin.display(description=_("Klasyfikacja"), boolean=True)
    def is_classified(self):
        """Check if the object has the unique related Group object."""
        return self.get_groups().count() == 1


class Employment(models.Model):
    """A class to represent the Employment objects."""

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        verbose_name=Employee._meta.verbose_name,
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        verbose_name=Position._meta.verbose_name,
        related_name="employments",
        blank=True,
        null=True,
    )
    subgroup = models.ForeignKey(
        Subgroup,
        on_delete=models.SET_NULL,
        verbose_name=Subgroup._meta.verbose_name,
        related_name="employments",
        blank=True,
        null=True,
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        verbose_name=Department._meta.verbose_name,
        related_name="employments",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("zatrudnienie")
        verbose_name_plural = _("zatrudnienia")
        ordering = ("id",)

    def __str__(self):
        return f"{_('Zatrudnienie')} ID={self.id}"
