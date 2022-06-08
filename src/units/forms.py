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

    university = forms.ModelChoiceField(
        queryset=University.objects.all(),
        label=University._meta.verbose_name.capitalize(),
        required=True,
    )


class FacultyModelChoiceField(forms.ModelChoiceField):
    """Customized model choice field for 'faculty' field of the Department model."""

    def label_from_instance(self, obj):
        return obj.name


class DepartmentAdminForm(forms.ModelForm):
    """A class to represent admin change form of the Department model."""

    class Meta:
        model = Department
        fields = "__all__"

    university = forms.ModelChoiceField(
        queryset=University.objects.all(),
        label=University._meta.verbose_name.capitalize(),
        required=True,
    )
    faculty = FacultyModelChoiceField(
        queryset=Faculty.objects.all(),
        label=Faculty._meta.verbose_name.capitalize(),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk is not None:
            self.fields["university"].initial = self.instance.faculty.university
