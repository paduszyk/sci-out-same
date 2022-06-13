from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Publisher(models.Model):
    """A class to represent Publisher objects."""

    name = models.CharField(_("tytuł"), max_length=255)
    abbreviation = models.CharField(_("skrót"), max_length=255, blank=True)
    international = models.BooleanField(_("międzynarodowe"), default=False)

    class Meta:
        verbose_name = _("wydawnictwo")
        verbose_name_plural = _("wydawnictwa")
        ordering = ("id",)

    def __str__(self):
        abbreviation = f"({self.abbreviation})" if self.abbreviation else ""
        return " ".join(filter(None, [self.name, abbreviation]))


class Journal(models.Model):
    """A class to represent Journal objects."""

    publisher = models.ForeignKey(
        to=Publisher,
        on_delete=models.SET_NULL,
        verbose_name=Publisher._meta.verbose_name,
        blank=True,
        null=True,
    )
    title = models.CharField(_("tytuł"), max_length=255)
    abbreviation = models.CharField(_("skrót"), max_length=255, blank=True)
    issn = models.CharField(
        _("ISSN"),
        max_length=9,
        blank=True,
        validators=[RegexValidator(r"[0-9]{4}-[0-9]{3}[0-9xX]")],
        error_messages={
            "invalid": _("Niepoprawny format numeru ISSN."),
            "unique": _("Istnieje już czasopismo z takim numerem ISSN."),
        },
        help_text=_(
            "ISSN wersji elektronicznej (e-ISSN). "
            "Jeśli nie istnieje, proszę podać ISSN wersji drukowanej (p-ISSN)."
        ),
    )
    ancestor = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        verbose_name=_("poprzednik"),
        related_name="successor_set",
        blank=True,
        null=True,
    )
    impact_factor = models.DecimalField(
        _("Impact Factor"),
        max_digits=6,
        decimal_places=3,
        default=0.0,
        validators=[MinValueValidator(0.0)],
        error_messages={
            "blank": _(
                "To pole nie może być puste. "
                "Jeśli czasopismo nie posiada IF, proszę wpisać 0."
            ),
            "min_value": _("Wartość IF musi być większa lub równa 0."),
        },
    )
    points = models.IntegerField(
        _("punkty"),
        default=0,
        validators=[MinValueValidator(0)],
        error_messages={
            "blank": _(
                "To pole nie może być puste. "
                "Jeśli czasopisma nie znajduje się na listach MEiN, proszę wpisać 0."
            ),
            "min_value": _("Liczba punktów musi być większa lub równa 0."),
        },
    )

    class Meta:
        verbose_name = _("czasopismo")
        verbose_name_plural = _("czasopisma")
        ordering = ("id",)

    def __str__(self):
        publisher = (
            f"({self.publisher.abbreviation or self.publisher.name})"
            if self.publisher
            else ""
        )
        return " ".join(filter(None, [self.title, publisher])).strip()

    def clean(self):
        if self.ancestor == self:
            raise ValidationError(
                {"ancestor": _("Czasopismo nie być swoim poprzednikiem.")}
            )

    def is_international(self):
        return getattr(self.publisher, "international", None)


class Article(models.Model):
    """A class to represent Article objects."""

    title = models.TextField(_("tytuł"))
    journal = models.ForeignKey(
        to=Journal,
        on_delete=models.CASCADE,
        verbose_name=Journal._meta.verbose_name,
    )
    year = models.PositiveSmallIntegerField(
        _("rok wydania"),
        validators=[MaxValueValidator(timezone.now().year + 1)],
        error_messages={
            "max_value": _(
                "Nie można dodać artykułu opublikowanego później niż "
                "w %(limit_value)s roku."
            )
        },
    )
    volume = models.CharField(_("wolumin"), max_length=255, blank=True)
    issue = models.CharField(_("wydanie/numer"), max_length=255, blank=True)
    first_page = models.CharField(_("pierwsza strona"), max_length=255, blank=True)
    last_page = models.CharField(_("ostatnia strona"), max_length=255, blank=True)
    doi = models.CharField(
        _("DOI"),
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        default=None,
        validators=[RegexValidator(r"10.\d{4,9}/[-._;()/:a-zA-Z0-9]+")],
        error_messages={"invalid": _("Niepoprawny format DOI.")},
    )
    url = models.URLField(
        _("URL"),
        blank=True,
        help_text=_(
            "Jeśli podano DOI, podany URL zostanie nadpisany tym powiązanym z DOI."
        ),
    )

    locked = models.BooleanField(_("zablokowany"), default=False)
    impact_factor = models.DecimalField(
        Journal._meta.get_field("impact_factor").verbose_name,
        max_digits=6,
        decimal_places=3,
        editable=False,
    )
    points = models.IntegerField(
        Journal._meta.get_field("points").verbose_name,
        editable=False,
    )

    class Meta:
        verbose_name = _("artykuł")
        verbose_name_plural = _("artykuły")
        ordering = ("id",)

    def __str__(self):
        return "{}. {}; {}.".format(
            self.title,
            self.journal.abbreviation or self.journal.title,
            ", ".join(
                filter(
                    None,
                    [
                        str(self.year),
                        self.get_volume_issue_str(),
                        self.get_pages_str(),
                    ],
                )
            ),
        )

    def clean(self):
        if self.last_page and not self.first_page:
            raise ValidationError(
                {
                    "first_page": _(
                        "Jeśli podano ostatnią stronę, należy również podać pierwszą."
                    )
                },
            )

        if self.first_page == self.last_page:
            self.last_page = ""

        self.url = "" if self.doi and self.url else self.url

        if not self.locked:
            self.impact_factor, self.points = (
                self.journal.impact_factor,
                self.journal.points,
            )

    def get_volume_issue_str(self):
        return "{} {}".format(
            self.volume or self.issue,
            f"({self.issue})" if self.issue and self.volume else "",
        ).strip()

    def get_pages_str(self):
        return "{}{}{}".format(
            self.first_page,
            "-" if self.last_page else "",
            self.last_page if self.last_page else "",
        )

    def get_url(self):
        return f"https://doi.org/{self.doi}" if self.doi else self.url
