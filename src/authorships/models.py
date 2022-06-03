from django.contrib import admin
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from employees.models import Employee


class Author(models.Model):
    """A class to represent authors."""

    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        verbose_name=Employee._meta.verbose_name,
        related_name="authors",
        blank=True,
        null=True,
    )
    alias = models.CharField(_("alias"), max_length=255)

    class Meta:
        verbose_name = _("autor")
        verbose_name_plural = _("autorzy")
        ordering = ("id",)

    class Manager(models.Manager):
        def get_queryset(self):
            """Get the annotated queryset."""
            return (
                super()
                .get_queryset()
                .annotate(authorship_count=models.Count("authorships", distinct=True))
            )

    objects = Manager()

    def __str__(self):
        return f"{self.alias}{f' ({self.employee})' if self.employee else ''}"

    def is_employed(self):
        """Return True if the author is also an employee."""
        return self.employee is not None

    @admin.display(description=_("Autorstwa"), ordering="authorship_count")
    def get_authorship_count(self):
        """Return the number of authorships related to the object."""
        return self.authorship_count


class Authorship(models.Model):
    """A class to represent authorships."""

    order = models.PositiveSmallIntegerField(_("numer"), default=1)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        verbose_name=Author._meta.verbose_name,
        related_name="authorships",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_("typ obiektu"),
    )
    object_id = models.PositiveIntegerField(verbose_name=_("ID obiektu"))
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = _("autorstwo")
        verbose_name_plural = _("autorstwa")
        ordering = ("id",)

    @admin.display(description=_("Alias"), ordering="author__alias")
    def get_alias(self):
        """Return the author's alias."""
        return self.author.alias

    @admin.display(description=_("Pracownik"), boolean=True)
    def by_employee(self):
        """Return True if the author is also an employee."""
        return self.author.is_employed()
