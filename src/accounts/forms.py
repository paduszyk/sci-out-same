from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

from .widgets import ImageInput


class LoginForm(AuthenticationForm):
    """A class to represent the user login form."""

    class Meta:
        model = get_user_model()
        fields = ("username", "password", "remember_me")

    remember_me = forms.BooleanField(
        label=_("Zapamiętaj mnie"),
        required=False,
        initial=False,
    )


class ProfileForm(forms.ModelForm):
    """A class to represent the user profile update form."""

    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email", "sex", "photo")
        widgets = {"photo": ImageInput}
