from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from employees.models import Employee
from units.models import Department

from ..articles.models import Article


class Author(models.Model):
    """A class to represent Author objects."""

    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        verbose_name=Employee._meta.verbose_name,
        blank=True,
        null=True,
    )
    alias = models.CharField(_("alias"), max_length=255, blank=True)

    class Meta:
        verbose_name = _("autor")
        verbose_name_plural = _("autorzy")
        ordering = ("id",)

    def __str__(self):
        return self.alias

    def clean(self):
        if not self.employee and not self.alias:
            raise ValidationError(
                _(
                    "Nie można utworzyć autora bez podania aliasu "
                    "oraz bez wskazania pracownika."
                )
            )
        if self.employee and not self.alias:
            self.alias = self.employee.get_short_name()

    def is_employed(self):
        """Return True if the author is also an employee."""
        return self.employee is not None


class ContributionStatus(models.Model):
    """A class to represent ContributionStatus objects."""

    name = models.CharField(_("nazwa"), max_length=255)
    code = models.CharField(_("skrót"), max_length=255)

    class Meta:
        verbose_name = _("status udziału")
        verbose_name_plural = _("statusy udziału")
        ordering = ("id",)

    def __str__(self):
        return f"{self.name} ({self.code})"


class AbstractContribution(models.Model):
    """A class to represent Contribution objects."""

    order = models.PositiveSmallIntegerField(_("Nr udziału"), default=1)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        verbose_name=Author._meta.verbose_name,
    )
    status = models.ForeignKey(
        ContributionStatus,
        on_delete=models.SET_NULL,
        verbose_name=ContributionStatus._meta.verbose_name,
        blank=True,
        null=True,
    )
    affiliation = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        verbose_name=_("afiliacja"),
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True
        ordering = ("id",)

    @property
    @admin.display(description=_("Alias"), ordering="author__alias")
    def alias(self):
        """Return the author's alias."""
        return self.author.alias

    @admin.display(description=_("Pracownik"), boolean=True)
    def is_by_employee(self):
        """Return if the contribution is by the author associated with Employee."""
        return self.author.is_employed()


class ArticleContribution(AbstractContribution):
    """A class to represent ArticleContribution objects."""

    article = models.ForeignKey(
        to=Article,
        on_delete=models.CASCADE,
        verbose_name=Article._meta.verbose_name,
        related_name="contribution_set",
    )

    corresponding_author = models.BooleanField(
        _("autor korespondencyjny"),
        default=False,
    )
    percentage = models.IntegerField(_("udział %"), default=0)

    class Meta(AbstractContribution.Meta):
        verbose_name = _("udział w artykule")
        verbose_name_plural = _("udziały w artykułach")
