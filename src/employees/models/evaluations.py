from django.db import models
from django.utils.translation import gettext_lazy as _


class Domain(models.Model):
    """A class to represent the Domain objects."""

    name = models.CharField(_("nazwa"), max_length=255)

    class Meta:
        verbose_name = _("dziedzina")
        verbose_name_plural = _("dziedziny")
        ordering = ("id",)

    class Manager(models.Manager):
        def get_queryset(self):
            """Update the queryset by some annotations."""
            return (
                super()
                .get_queryset()
                .annotate(
                    discipline_count=models.Count(
                        "disciplines",
                        distinct=True,
                    ),
                    employee_count=models.Count(
                        "disciplines__employees",
                        distinct=True,
                    ),
                )
            )

    objects = Manager()

    def __str__(self):
        return self.name


class Discipline(models.Model):
    """A class to represent the Discipline objects."""

    domain = models.ForeignKey(
        Domain,
        on_delete=models.CASCADE,
        verbose_name=Domain._meta.verbose_name,
        related_name="disciplines",
    )
    name = models.CharField(_("nazwa"), max_length=255)
    abbr = models.CharField(_("skrót"), max_length=255)

    class Meta:
        verbose_name = _("dyscyplina")
        verbose_name_plural = _("dyscypliny")
        ordering = ("id",)

    class Manager(models.Manager):
        def get_queryset(self):
            """Update the queryset by some annotations."""
            return (
                super()
                .get_queryset()
                .annotate(
                    employee_count=models.Count(
                        "employees",
                        distinct=True,
                    )
                )
            )

    objects = Manager()

    def __str__(self):
        return self.name
