from django.forms import widgets
from django.utils.translation import gettext_lazy as _


class ImageInput(widgets.ClearableFileInput):
    """A class to represent a customized image-upload widget."""

    template_name = "forms/widgets/image_input.html"
    clear_checkbox_label = _("Usuń zdjęcie po zapisaniu formularza")
