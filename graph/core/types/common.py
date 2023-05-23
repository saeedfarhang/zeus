from urllib.parse import urljoin
from django.conf import settings
import graphene

from graph.core.enums import (
    CafeCanvasErrorCode,
    CafeErrorCode,
    MenuErrorCode,
    ProvinceErrorCode,
    CityErrorCode,
)
from graph.core.utils.images import get_thumbnail


class Image(graphene.ObjectType):
    url = graphene.String(required=True, description="The URL of the image.")
    alt = graphene.String(description="Alt text for an image.")

    class Meta:
        description = "Represents an image."

    @staticmethod
    def get_adjusted(image, alt, size, rendition_key_set, info):
        """Return Image adjusted with given size."""
        if size:
            url = get_thumbnail(
                image_file=image,
                size=size,
                method="thumbnail",
                rendition_key_set=rendition_key_set,
            )
        else:
            url = image.url
        url = info.context.build_absolute_uri(url)
        return Image(url, alt)


class File(graphene.ObjectType):
    url = graphene.String(required=True, description="The URL of the file.")
    content_type = graphene.String(
        required=False, description="Content type of the file."
    )

    @staticmethod
    def resolve_url(root, info):
        return info.context.build_absolute_uri(urljoin(settings.MEDIA_URL, root.url))


class NonNullList(graphene.List):
    """A list type that automatically adds non-null constraint on contained items."""

    def __init__(self, of_type, *args, **kwargs):
        of_type = graphene.NonNull(of_type)
        super(NonNullList, self).__init__(of_type, *args, **kwargs)


class Error(graphene.ObjectType):
    field = graphene.String(
        description=(
            "Name of a field that caused the error. A value of `null` indicates that "
            "the error isn't associated with a particular field."
        ),
        required=False,
    )
    message = graphene.String(description="The error message.")

    class Meta:
        description = "Represents an error in the input of a mutation."


class CafeCanvasError(Error):
    code = CafeCanvasErrorCode(description="The error code.", required=True)


class CafeTableError(Error):
    code = CafeCanvasErrorCode(description="The error code.", required=True)


class CafeError(Error):
    code = CafeErrorCode(description="The error code.", required=True)


class ProvinceError(Error):
    code = ProvinceErrorCode(description="The error code.", required=True)


class CityError(Error):
    code = CityErrorCode(description="The error code.", required=True)


class MenuError(Error):
    code = MenuErrorCode(description="The error code.", required=True)
