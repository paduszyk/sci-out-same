from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractUnit(models.Model):
    """
    A class to represent the abstracted units.

    All other models in this module inherit from this class.
    """

    name = models.CharField(_("nazwa"), max_length=255)
    abbr = models.CharField(_("skrót"), max_length=255, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class University(AbstractUnit):
    """A class to represent universities."""

    class Meta:
        verbose_name = _("uczelnia")
        verbose_name_plural = _("uczelnie")
        ordering = ("id",)

    class Manager(models.Manager):
        """A class customizing default model's manager."""

        def get_queryset(self):
            """Get the annotated queryset."""
            return (
                super()
                .get_queryset()
                .order_by("name")
                .annotate(
                    faculty_count=models.Count(
                        "faculties",
                        distinct=True,
                    ),
                    department_count=models.Count(
                        "faculties__departments",
                        distinct=True,
                    ),
                )
            )

    objects = Manager()

    @admin.display(description=_("Wydziały"), ordering="faculty_count")
    def get_faculty_count(self):
        """Return the number of faculties related to the object."""
        return self.faculty_count

    @admin.display(description=_("Katedry"), ordering="department_count")
    def get_department_count(self):
        """Return the number of departments related to all faculties of the object."""
        return self.department_count


class Faculty(AbstractUnit):
    """A class to represent faculties."""

    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        verbose_name=University._meta.verbose_name,
        related_name="faculties",
    )

    class Manager(models.Manager):
        """A class customizing default model's manager."""

        def get_queryset(self):
            """Get the annotated queryset."""
            return (
                super()
                .get_queryset()
                .order_by("name")
                .annotate(
                    department_count=models.Count(
                        "departments",
                        distinct=True,
                    ),
                )
            )

    objects = Manager()

    class Meta:
        verbose_name = _("wydział")
        verbose_name_plural = _("wydziały")
        ordering = ("id",)

    @admin.display(description=_("Katedry"), ordering="department_count")
    def get_department_count(self):
        """Return the number of departments related to the object."""
        return self.department_count


class Department(AbstractUnit):
    """A class to represent departments."""

    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        verbose_name=Faculty._meta.verbose_name,
        related_name="departments",
    )

    class Meta:
        verbose_name = _("katedra")
        verbose_name_plural = _("katedry")
        ordering = ("id",)
