from django import forms

from ..models import Employment, Group, Position, Subgroup


class GroupAdminForm(forms.ModelForm):
    """A class to represent admin change form of the Group model."""

    class Meta:
        model = Group
        fields = "__all__"


class SubgroupAdminForm(forms.ModelForm):
    """A class to represent admin change form of the Subgroup model."""

    class Meta:
        model = Subgroup
        fields = "__all__"


class PositionAdminForm(forms.ModelForm):
    """A class to represent admin change form of the Position model."""

    class Meta:
        model = Position
        fields = "__all__"


class EmploymentAdminForm(forms.ModelForm):
    """A class to represent admin change form of the Employment model."""

    class Meta:
        model = Employment
        fields = "__all__"
