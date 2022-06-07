from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractUnit(models.Model):
    """
    A class to represent the abstract unit objects.

    All other models in this module inherit from this class.
    """

    name = models.CharField(_("nazwa"), max_length=255)
    abbr = models.CharField(_("skrót"), max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class University(AbstractUnit):
    """A class to represent the University objects."""

    class Meta:
        verbose_name = _("uczelnia")
        verbose_name_plural = _("uczelnie")
        ordering = ("id",)

    class Manager(models.Manager):
        def get_queryset(self):
            """Update the queryset by some annotations."""
            return (
                super()
                .get_queryset()
                .annotate(
                    faculty_count=models.Count(
                        "faculties",
                        distinct=True,
                    ),
                    department_count=models.Count(
                        "faculties__departments",
                        distinct=True,
                    ),
                    employee_count=models.Count(
                        "faculties__departments__employments__employee",
                        distinct=True,
                    ),
                )
            )

    objects = Manager()


class Faculty(AbstractUnit):
    """A class to represent the Faculty objects."""

    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        verbose_name=University._meta.verbose_name,
        related_name="faculties",
    )

    class Manager(models.Manager):
        def get_queryset(self):
            """Update the queryset by some annotations."""
            return (
                super()
                .get_queryset()
                .annotate(
                    department_count=models.Count(
                        "departments",
                        distinct=True,
                    ),
                    employee_count=models.Count(
                        "departments__employments__employee",
                        distinct=True,
                    ),
                )
            )

    objects = Manager()

    class Meta:
        verbose_name = _("wydział")
        verbose_name_plural = _("wydziały")
        ordering = ("id",)


class Department(AbstractUnit):
    """A class to represent the Department objects."""

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

    @property
    @admin.display(
        description=University._meta.verbose_name.capitalize(),
        ordering="faculty__university",
    )
    def university(self):
        """Return the University object of the object's related Faculty."""
        return self.faculty.university
