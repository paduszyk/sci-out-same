from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from . import settings, utils


class User(AbstractUser):
    """
    A class to represent customized User model.

    Based on Django built-in django.contrib.auth AbstractUser, see:
    https://docs.djangoproject.com/en/4.0/topics/auth/customizing/
    """

    class SexChoices(models.TextChoices):
        """A class to represent choices for the sex field."""

        WOMAN = "W", _("kobieta")
        MAN = "M", _("mężczyzna")

    sex = models.CharField(
        _("płeć"),
        max_length=1,
        choices=SexChoices.choices,
        blank=True,
        null=True,
    )
    photo = models.ImageField(
        _("zdjęcie profilowe"),
        upload_to=utils.photo_upload_path,
        blank=True,
        null=True,
        help_text=_(
            f"Przesłane zdjęcie zostanie wykadrowane obszarem największego "
            "i wycentrowanego kwadratu oraz przeskalowane do rozmiaru "
            f"{settings.MEDIA_PHOTOS_SIZE} x {settings.MEDIA_PHOTOS_SIZE} px."
        ),
    )
    icon = models.ImageField(
        _("ikona"),
        upload_to=utils.icon_upload_path,
        blank=True,
        null=True,
        editable=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._meta.get_field("is_staff").verbose_name = _("administrator")

    def __str__(self):
        return f"{self.username} (ID = {self.id})"

    def get_full_name(self):
        """Return the user's full name."""
        if self.first_name or self.last_name:
            return super().get_full_name()
        else:
            return self.username

    def get_short_name(self):
        """Return the user's short name: the last name followed by initials."""
        initials = f"{self.first_name[0]}." if self.first_name else ""

        if initials or self.last_name:
            return f"{self.last_name} {initials}".strip()
        else:
            return self.username

    @admin.display(description=_("Pracownik"), boolean=True)
    def has_employee(self):
        """Return True if the user has an employee associated with it."""
        return self.employee is not None
