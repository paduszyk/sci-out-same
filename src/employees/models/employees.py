from django.conf import settings
from django.contrib import admin
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .evaluations import Discipline


class Status(models.Model):
    """A class to represent employee's statuses."""

    name = models.CharField(_("nazwa"), max_length=255)
    abbr = models.CharField(_("skrót"), max_length=255)

    class Meta:
        verbose_name = _("status")
        verbose_name_plural = _("statusy")
        ordering = ("id",)

    def __str__(self):
        return f"{self.name} ({self.abbr})"


class Degree(models.Model):
    """A class to represent employee's academic degrees."""

    abbr = models.CharField(_("skrót"), max_length=255)

    class Meta:
        verbose_name = _("stopień/tytuł naukowy")
        verbose_name_plural = _("stopnie i tytuły naukowe")
        ordering = ("abbr",)

    def __str__(self):
        return self.abbr


class Employee(models.Model):
    """A class to represent employees."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("użytkownik"),
    )
    slug = models.SlugField(_("slug"), max_length=255, unique=True)
    degree = models.ForeignKey(
        Degree,
        on_delete=models.SET_NULL,
        verbose_name=Degree._meta.verbose_name,
        related_name="employees",
        blank=True,
        null=True,
    )
    orcid = models.CharField(
        _("ORCID"),
        max_length=19,
        validators=[RegexValidator(r"^\d{4}-\d{4}-\d{4}-\d{3}(\d|X)$")],
        unique=True,
        blank=True,
        null=True,
        default=None,
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        verbose_name=Status._meta.verbose_name,
        related_name="employees",
    )
    in_evaluation = models.BooleanField(_("w liczbie N"), default=True)
    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.SET_NULL,
        verbose_name=Discipline._meta.verbose_name,
        related_name="employees",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("pracownik")
        verbose_name_plural = _("pracownicy")
        ordering = ("id",)

    def __str__(self):
        return self.user.get_full_name()

    @admin.display(description=_("Nazwisko"), ordering="user__last_name")
    def last_name(self):
        """Return the employee's last name."""
        return self.user.last_name

    @admin.display(description=_("Imię"), ordering="user__first_name")
    def first_name(self):
        """Return the employee's first name."""
        return self.user.first_name

    @admin.display(description=_("Zatrudniony"), boolean=True)
    def is_employed(self):
        """Return True if an employee has an employment associated."""
        return self.employment is not None
