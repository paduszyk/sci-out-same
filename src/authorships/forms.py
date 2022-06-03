from django import forms
from django.contrib.contenttypes.models import ContentType

from .models import Author, Authorship, AuthorshipType


class AuthorAdminForm(forms.ModelForm):
    """A class to represent admin change form of the Author model."""

    class Meta:
        model = Author
        fields = "__all__"


class AuthorshipTypeAdminForm(forms.ModelForm):
    """A class to represent admin change form of the Authorship model."""

    class Meta:
        model = AuthorshipType
        fields = "__all__"


class AuthorshipAdminForm(forms.ModelForm):
    """A class to represent admin change form of the Authorship model."""

    class ContentTypeModelChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            """Override an instance label for the ContentType objects."""
            return obj.name

    class Meta:
        model = Authorship
        fields = "__all__"

    content_type = ContentTypeModelChoiceField(
        queryset=ContentType.objects.all(),
        label=Authorship._meta.get_field("content_type").verbose_name.capitalize(),
        required=True,
    )
