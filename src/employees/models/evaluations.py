from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _


class Domain(models.Model):
    """A class to represent domains of science."""

    name = models.CharField(_("nazwa"), max_length=255)

    class Meta:
        verbose_name = _("dziedzina")
        verbose_name_plural = _("dziedziny")
        ordering = ("id",)

    class Manager(models.Manager):
        """A class customizing default model's manager."""

        def get_queryset(self):
            """Get the annotated queryset."""
            return (
                super()
                .get_queryset()
                .annotate(discipline_count=models.Count("disciplines", distinct=True))
            )

    objects = Manager()

    def __str__(self):
        return self.name

    @admin.display(description=_("Dyscypliny"), ordering="discipline_count")
    def get_discipline_count(self):
        """Return the number of disciplines related to the object."""
        return self.discipline_count


class Discipline(models.Model):
    """A class to represent disciplines within given domain of science."""

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

    def __str__(self):
        return f"{self.name} ({self.domain})"
