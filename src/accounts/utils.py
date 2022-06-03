import os
import uuid

from . import settings


def photo_upload_path(instance, file_name):
    """Return path of the user's photo file uploaded to media root."""
    _, file_ext = os.path.splitext(file_name)

    return os.path.join(settings.MEDIA_PHOTOS_DIR, str(uuid.uuid4()) + file_ext)


def icon_upload_path(instance, file_name):
    """Return path of the user's icon file uploaded to media root."""
    _, file_ext = os.path.splitext(file_name)

    return os.path.join(settings.MEDIA_ICONS_DIR, str(uuid.uuid4()) + file_ext)
