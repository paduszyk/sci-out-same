from django import forms

from ..models import Degree, Employee, Status


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


class EmployeeAdminForm(forms.ModelForm):
    """A class to represent admin change form of the Employee model."""

    class Meta:
        model = Employee
        fields = "__all__"
