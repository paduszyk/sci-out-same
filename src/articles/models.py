from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

from authorships.models import Author, Authorship


class Journal(models.Model):
    """A class to represent the Journal objects."""

    title = models.CharField(_("tytuł"), max_length=255)
    abbr = models.CharField(_("skrót"), max_length=255)
    ancestor = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name=_("przodek"),
        related_name="successors",
        blank=True,
        null=True,
    )
    impact_factor = models.DecimalField(
        _("IF"),
        max_digits=6,
        decimal_places=3,
        blank=True,
        null=True,
    )
    points = models.PositiveSmallIntegerField(_("punkty"), blank=True, null=True)

    class Meta:
        verbose_name = _("czasopismo")
        verbose_name_plural = _("czasopisma")
        ordering = ("id",)

    class Manager(models.Manager):
        def get_queryset(self):
            """Update the queryset by some annotations."""
            return (
                super()
                .get_queryset()
                .annotate(
                    article_count=models.Count(
                        "articles",
                        distinct=True,
                    )
                )
            )

    objects = Manager()

    def __str__(self):
        return self.title


class Article(models.Model):
    """A class to represent the Article objects."""

    title = models.TextField(_("tytuł"))
    journal = models.ForeignKey(
        Journal,
        on_delete=models.CASCADE,
        verbose_name=Journal._meta.verbose_name,
        related_name="articles",
    )
    year = models.PositiveSmallIntegerField(_("rok"))
    volume = models.CharField(_("wolumin"), max_length=255, blank=True, null=True)
    pages = models.CharField(_("strony"), max_length=255, blank=True, null=True)
    doi = models.CharField(_("DOI"), max_length=255, blank=True, null=True)
    impact_factor = models.DecimalField(
        _("IF"),
        max_digits=6,
        decimal_places=3,
        blank=True,
        null=True,
        editable=False,
    )
    points = models.PositiveSmallIntegerField(
        _("punkty"),
        blank=True,
        null=True,
        editable=False,
    )
    locked = models.BooleanField(_("zablokowany"), default=False)

    authorships = GenericRelation(Authorship)

    authors = models.TextField(
        Author._meta.verbose_name_plural,
        editable=False,
        blank=True,
        null=True,
    )
    author_count = models.PositiveSmallIntegerField(
        _("liczba autorów"),
        editable=False,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("artykuł")
        verbose_name_plural = _("artykuły")
        ordering = ("id",)

    def __str__(self):
        return f"{self.title} ({self.year}; {self.journal})"

    def clean(self):
        """Run some model-wide checks and updates."""
        if not self.locked:
            self.impact_factor, self.points = (
                self.journal.impact_factor,
                self.journal.points,
            )

    def get_authors(self):
        """Get a list of the Author objects associated with the object authorships."""
        return [authorship.author for authorship in self.authorships.order_by("order")]
