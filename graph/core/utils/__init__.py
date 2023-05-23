import os
import secrets
from django.core.exceptions import ValidationError
from PIL import Image


def is_image_mimetype(mimetype: str) -> bool:
    """Check if mimetype is image."""
    if mimetype is None:
        return False
    return mimetype.startswith("image/")


def validate_image_file(file, field_name, error_class) -> None:
    """Validate if the file is an image."""
    if not file:
        raise ValidationError(
            {
                field_name: ValidationError(
                    "File is required.", code=error_class.REQUIRED
                )
            }
        )
    if not is_image_mimetype(file.content_type):
        raise ValidationError(
            {
                field_name: ValidationError(
                    "Invalid file type.", code=error_class.INVALID
                )
            }
        )
    _validate_image_format(file, field_name, error_class)


def _validate_image_format(file, field_name, error_class):
    """Validate image file format."""
    allowed_extensions = [ext.lower() for ext in Image.EXTENSION]
    _file_name, format = os.path.splitext(file._name)
    if not format:
        raise ValidationError(
            {
                field_name: ValidationError(
                    "Lack of file extension.", code=error_class.INVALID
                )
            }
        )
    elif format not in allowed_extensions:
        raise ValidationError(
            {
                field_name: ValidationError(
                    "Invalid file extension. Image file required.",
                    code=error_class.INVALID,
                )
            }
        )


def add_hash_to_file_name(file):
    """Add unique text fragment to the file name to prevent file overriding."""
    file_name, format = os.path.splitext(file._name)
    hash = secrets.token_hex(nbytes=4)
    new_name = f"{file_name}_{hash}{format}"
    file._name = new_name
