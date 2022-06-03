from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _

from units.models import Department


class Group(models.Model):
    """A class to represent groups of positions."""

    name = models.CharField(_("nazwa"), max_length=255)
    abbr = models.CharField(_("skrót"), max_length=255)

    class Meta:
        verbose_name = _("grupa pracowników")
        verbose_name_plural = _("grupy pracowników")
        ordering = ("id",)

    def __str__(self):
        return self.name


class Subgroup(models.Model):
    """A class to represent subgroups of positions within a group."""

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

    def __str__(self):
        return f"{self.name} ({self.group})"


class Position(models.Model):
    """A class to represent positions."""

    name = models.CharField(_("nazwa"), max_length=255)
    subgroups = models.ManyToManyField(
        Subgroup,
        verbose_name=Subgroup._meta.verbose_name_plural,
    )

    class Meta:
        verbose_name = _("stanowisko")
        verbose_name_plural = _("stanowiska")
        ordering = ("id",)

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
        """Check if the position has unique group."""
        return self.get_groups().count() == 1


class Employment(models.Model):
    """A class to represent employments."""

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
        return ""
