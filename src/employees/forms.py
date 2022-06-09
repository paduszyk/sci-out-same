from django import forms

from .models import (
    Degree,
    Discipline,
    Domain,
    Employee,
    Employment,
    Group,
    Position,
    Status,
    Subgroup,
)


class StatusAdminForm(forms.ModelForm):
    """A class to represent admin change form of the Status model."""

    class Meta:
        model = Status
        fields = "__all__"


class DegreeAdminForm(forms.ModelForm):
    """A class to represent admin change form of the Degree model."""

    class Meta:
        model = Degree
        fields = "__all__"


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


class EmployeeAdminForm(forms.ModelForm):
    """A class to represent admin change form of the Employee model."""

    class Meta:
        model = Employee
        fields = "__all__"


class EmploymentAdminForm(forms.ModelForm):
    """A class to represent admin change form of the Employment model."""

    class Meta:
        model = Employment
        fields = "__all__"
