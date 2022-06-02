from django import forms

from .models import Department, Faculty, University


class UniversityAdminForm(forms.ModelForm):
    """A class to represent admin change form of the University model."""

    class Meta:
        model = University
        fields = "__all__"


class FacultyAdminForm(forms.ModelForm):
    """A class to represent admin change form of the Faculty model."""

    class Meta:
        model = Faculty
        fields = "__all__"


class DepartmentAdminForm(forms.ModelForm):
    """A class to represent admin change form of the Department model."""

    class Meta:
        model = Department
        fields = "__all__"
