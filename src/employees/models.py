from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from units.models import Department


class Status(models.Model):
    """A class to represent the Status objects."""

    name = models.CharField(_("nazwa"), max_length=255)
    code = models.CharField(_("kod"), max_length=2)

    class Meta:
        verbose_name = _("status")
        verbose_name_plural = _("statusy")
        ordering = ("id",)

    def __str__(self):
        return f"{self.name} ({self.code})"

    def clean(self):
        """Run pre-save validation and updates of the model instance."""
        self.code = self.code.upper()


class Degree(models.Model):
    """A class to represent the Degree objects."""

    code = models.CharField(_("skrót"), max_length=255)

    class Meta:
        verbose_name = _("stopień/tytuł naukowy")
        verbose_name_plural = _("stopnie i tytuły naukowe")
        ordering = ("id",)

    def __str__(self):
        return self.code


class Domain(models.Model):
    """A class to represent the Domain objects."""

    name = models.CharField(_("nazwa"), max_length=255)
    code = models.CharField(_("kod"), max_length=2)

    class Meta:
        verbose_name = _("dziedzina nauki")
        verbose_name_plural = _("dziedziny nauki")
        ordering = ("id",)

    def __str__(self):
        return self.name

    def clean(self):
        """Run pre-save validation and updates of the model instance."""
        self.code = self.code.upper()


class Discipline(models.Model):
    """A class to represent Discipline objects."""

    name = models.CharField(_("nazwa"), max_length=255)
    code = models.CharField(_("kod"), max_length=2)
    domain = models.ForeignKey(
        to=Domain,
        on_delete=models.CASCADE,
        verbose_name=Domain._meta.verbose_name,
    )

    class Meta:
        verbose_name = _("dyscyplina nauki")
        verbose_name_plural = _("dyscypliny nauki")
        ordering = ("id",)

    def __str__(self):
        return self.name

    def clean(self):
        """Run pre-save validation and updates of the model instance."""
        self.code = self.code.upper()


class Group(models.Model):
    """A class to represent the Group objects."""

    name = models.CharField(_("nazwa"), max_length=255)
    code = models.CharField(_("kod"), max_length=2)

    class Meta:
        verbose_name = _("grupa")
        verbose_name_plural = _("grupy")
        ordering = ("id",)

    def __str__(self):
        return self.name

    def clean(self):
        """Run pre-save validation and updates of the model instance."""
        self.code = self.code.upper()


class Subgroup(models.Model):
    """A class to represent the Subgroup objects."""

    group = models.ForeignKey(
        to=Group,
        on_delete=models.CASCADE,
        verbose_name=Group._meta.verbose_name,
    )
    name = models.CharField(_("nazwa"), max_length=255)
    code = models.CharField(_("kod"), max_length=2)

    class Meta:
        verbose_name = _("podgrupa")
        verbose_name_plural = _("podgrupy")
        ordering = ("id",)

    def __str__(self):
        return self.name

    def clean(self):
        """Run pre-save validation and updates of the model instance."""
        self.code = self.code.upper()


class Position(models.Model):
    """A class to represent the Position objects."""

    subgroup_set = models.ManyToManyField(
        to=Subgroup,
        verbose_name=Subgroup._meta.verbose_name_plural,
        blank=True,
    )
    name = models.CharField(_("nazwa"), max_length=255)

    class Meta:
        verbose_name = _("stanowisko")
        verbose_name_plural = _("stanowiska")
        ordering = ("id",)

    def __str__(self):
        return self.name

    @property
    @admin.display(description=Group._meta.verbose_name.capitalize())
    def group(self):
        """Return the Group object related to the object via `subgroups` field."""
        if self.subgroup_set.exists():
            return self.subgroup_set.first().group


User = get_user_model()


class Employee(models.Model):
    """A class to represent the Employee objects."""

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        verbose_name=User._meta.verbose_name,
    )
    status = models.ForeignKey(
        to=Status,
        on_delete=models.CASCADE,
        verbose_name=Status._meta.verbose_name,
        blank=True,
        null=True,
    )
    degree = models.ForeignKey(
        to=Degree,
        on_delete=models.SET_NULL,
        verbose_name=Degree._meta.verbose_name,
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
    in_evaluation = models.BooleanField(_("w liczbie N"), default=False)
    discipline = models.ForeignKey(
        to=Discipline,
        on_delete=models.SET_NULL,
        verbose_name=Discipline._meta.verbose_name,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("pracownik")
        verbose_name_plural = _("pracownicy")
        ordering = ("id",)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return self.user.get_full_name()

    def get_short_name(self):
        return self.user.get_short_name()

    @property
    @admin.display(description=_("Nazwisko"), ordering="user__last_name")
    def last_name(self):
        return self.user.last_name

    @property
    @admin.display(description=_("Imię"), ordering="user__first_name")
    def first_name(self):
        return self.user.first_name

    @property
    def email(self):
        return self.user.email

    @property
    def positions(self):
        return [employment.position for employment in self.employment_set.all()]

    @property
    def subgroups(self):
        return [employment.subgroup for employment in self.employment_set.all()]

    @property
    def departments(self):
        return [employment.department for employment in self.employment_set.all()]


class Employment(models.Model):
    """A class to represent the Employment objects."""

    employee = models.ForeignKey(
        to=Employee,
        on_delete=models.CASCADE,
        verbose_name=Employee._meta.verbose_name,
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        verbose_name=Position._meta.verbose_name,
        blank=True,
        null=True,
    )
    subgroup = models.ForeignKey(
        Subgroup,
        on_delete=models.SET_NULL,
        verbose_name=Subgroup._meta.verbose_name,
        blank=True,
        null=True,
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        verbose_name=Department._meta.verbose_name,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("zatrudnienie")
        verbose_name_plural = _("zatrudnienia")
        ordering = ("id",)

    def __str__(self):
        return f"{self._meta.verbose_name.capitalize()} ID={self.id}"
