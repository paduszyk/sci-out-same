from io import BytesIO

from django.core.files.base import ContentFile
from django.db.models import signals
from django.dispatch import receiver

from PIL import Image

from . import settings
from .models import User


@receiver(signals.post_save, sender=User)
def crop_and_resize_profile_photo(sender, instance, **kwargs):
    """
    Post-process the photo submitted by the user by using pillow.

    The photo is cropped to the area of the largest-centered square and resized.
    """
    if not instance.photo:
        return None

    with Image.open(instance.photo.path) as photo:
        # Determine the cropping area coordinates depending on the photo shape
        width, height = photo.size
        if height > width:  # portrait
            box = (0, int((height - width) / 2), width, int((height + width) / 2))
        elif height < width:  # landscape
            box = (int((width - height) / 2), 0, int((width + height) / 2), height)
        else:
            box = (0, 0, width, height)

        # Crop & resize, then overwrite the original photo
        new_photo = photo.crop(box=box).resize(size=settings.MEDIA_PHOTOS_SIZE)
        new_photo.save(instance.photo.path)


@receiver(signals.post_save, sender=User)
def create_profile_icon(sender, instance, **kwargs):
    """
    Create and save the icon of the user.

    The icon is simply a smaller version of the user's cropped & resized photo.
    """
    if instance.photo:
        if instance.icon:
            return None

        with Image.open(instance.photo.path) as photo:
            icon = photo.resize(size=settings.MEDIA_ICONS_SIZE)

            with BytesIO() as icon_file:
                icon.save(icon_file, format=photo.format)
                icon_file.seek(0)

                if not instance.icon:
                    instance.icon.save(
                        instance.photo.name,  # only to retrieve the file extension
                        ContentFile(icon_file.read()),
                        save=True,
                    )
                else:
                    # Note that instance has been just saved within post_save
                    # signal. Therefore, do nothing if the icon field has been
                    # already populated. Otherwise, RecursionError is raised.
                    pass
    else:
        # If there is no photo but icon, remove the icon file as well
        if instance.icon:
            instance.icon.delete(save=True)
