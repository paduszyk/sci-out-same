import os
import uuid

# User photo and icon dirs and sizes

MEDIA_PHOTOS_DIR = os.path.join(__package__, "photos")
MEDIA_PHOTOS_SIZE = (512, 512)

MEDIA_ICONS_DIR = os.path.join(__package__, "icons")
MEDIA_ICONS_SIZE = (32, 32)


def photo_upload_path(instance, file_name):
    """Return path of the user's photo file uploaded to media root."""
    _, file_ext = os.path.splitext(file_name)

    return os.path.join(MEDIA_PHOTOS_DIR, str(uuid.uuid4()) + file_ext)


def icon_upload_path(instance, file_name):
    """Return path of the user's icon file uploaded to media root."""
    _, file_ext = os.path.splitext(file_name)

    return os.path.join(MEDIA_ICONS_DIR, str(uuid.uuid4()) + file_ext)
