from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractUnit(models.Model):
    """A class to represent AbstractUnit objects."""

    name = models.CharField(_("nazwa"), max_length=255)
    code = models.CharField(_("skrót"), max_length=255)

    class Meta:
        abstract = True
        ordering = ("id",)

    def __str__(self):
        return self.get_full_name()

    def _get_parent(self):
        return None

    def _get_parents(self):
        units = [self._get_parent()]

        while units[-1] is not None:
            units.append(units[-1]._get_parent())
        units.pop()

        return units

    def _get_full_info(self, field, delimiter):
        return delimiter.join(
            [getattr(unit, field) for unit in [self] + self._get_parents()],
        )

    def get_full_name(self, delimiter=", "):
        return self._get_full_info("name", delimiter)

    def get_full_code(self, delimiter=" / "):
        return self._get_full_info("code", delimiter)


class University(AbstractUnit):
    """A class to represent University objects."""

    class Meta(AbstractUnit.Meta):
        verbose_name = _("uczelnia")
        verbose_name_plural = _("uczelnie")


class Faculty(AbstractUnit):
    """A class to represent Faculty objects."""

    university = models.ForeignKey(
        to=University,
        on_delete=models.CASCADE,
        verbose_name=University._meta.verbose_name,
    )

    class Meta(AbstractUnit.Meta):
        verbose_name = _("wydział")
        verbose_name_plural = _("wydziały")

    def _get_parent(self):
        return self.university


class Department(AbstractUnit):
    """A class to represent Department objects."""

    faculty = models.ForeignKey(
        to=Faculty,
        on_delete=models.CASCADE,
        verbose_name=Faculty._meta.verbose_name,
    )

    class Meta(AbstractUnit.Meta):
        verbose_name = _("katedra")
        verbose_name_plural = _("katedry")

    def _get_parent(self):
        return self.faculty

    @property
    def university(self):
        return self.faculty.university
