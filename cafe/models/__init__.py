from .cafe import Cafe
from .cafe_map import CafeCanvas, Point, CafeElement


class MediaTypes:
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"

    CHOICES = [
        (IMAGE, "An uploaded image or an URL to an image"),
        (VIDEO, "A URL to an external video"),
    ]
