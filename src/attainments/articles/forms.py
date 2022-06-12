from django import forms

from .models import Article, Journal, Publisher


class PublisherAdminForm(forms.ModelForm):
    """A class to represent admin change form of the Publisher model."""

    class Meta:
        model = Publisher
        fields = "__all__"


class JournalAdminForm(forms.ModelForm):
    """A class to represent admin change form of the Journal model."""

    class Meta:
        model = Journal
        fields = "__all__"


class ArticleAdminForm(forms.ModelForm):
    """A class to represent admin change form of the Article model."""

    class Meta:
        model = Article
        fields = "__all__"
