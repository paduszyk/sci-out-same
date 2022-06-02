from django import forms

from ..models import Discipline, Domain


class DomainAdminForm(forms.ModelForm):
    """A class to represent admin change form of the Domain model."""

    class Meta:
        model = Domain
        fields = "__all__"


class DisciplineAdminForm(forms.ModelForm):
    """A class to represent admin change form of the Discipline model."""

    class Meta:
        model = Discipline
        fields = "__all__"
