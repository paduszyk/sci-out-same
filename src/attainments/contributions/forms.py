from django import forms

from .models import ArticleContribution, Author, ContributionStatus


class AuthorAdminForm(forms.ModelForm):
    """A class to represent admin change form of the Author model."""

    class Meta:
        model = Author
        fields = "__all__"


class ContributionStatusAdminForm(forms.ModelForm):
    """A class to represent admin change form of the ContributionStatus model."""

    class Meta:
        model = ContributionStatus
        fields = "__all__"


class ArticleContributionAdminForm(forms.ModelForm):
    """A class to represent admin change form of the ArticleContribution model."""

    class Meta:
        model = ArticleContribution
        fields = "__all__"
