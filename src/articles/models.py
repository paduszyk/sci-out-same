from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _


class Journal(models.Model):
    """A class to represent journals."""

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
            """Get the annotated queryset."""
            return (
                super()
                .get_queryset()
                .annotate(article_count=models.Count("articles", distinct=True))
            )

    objects = Manager()

    def __str__(self):
        return self.title

    @admin.display(description=_("Artykuły"), ordering="article_count")
    def get_article_count(self):
        """Get the number of articles published in the journal."""
        return self.article_count


class Article(models.Model):
    """A class to represent articles."""

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

    class Meta:
        verbose_name = _("artykuł")
        verbose_name_plural = _("artykuły")
        ordering = ("id",)

    def __str__(self):
        return f"{self.title} ({self.year}; {self.journal})"
