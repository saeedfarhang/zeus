import graphene
from graphene_django import DjangoObjectType
from cafe.models import Cafe
from cafe.models.cafe_map import CafeCanvas, CafeTable, Point
from graph.core.types.common import Image
from graph.core.types.model import ModelObjectType
from graph.core.utils.images import get_thumbnail
from graph.locations.types import AddressInput, AddressType
from menu.models import Menu, MenuItem
from media_manager.models import Media


class SmokingFreeEnum(graphene.Enum):
    YES = "YES"
    NO = "NO"
    SMOKING_ROOM = "SMOKING_ROOM"
    SMOKING_SECTION = "SMOKING_SECTION"


class PointInput(graphene.InputObjectType):
    x = graphene.Int(default_value=0)
    y = graphene.Int(default_value=0)
    order = graphene.Int(default_value=0)


class CafeCanvasInput(graphene.InputObjectType):
    line_points = graphene.List(PointInput)


class AddCafeTableInput(graphene.InputObjectType):
    name = graphene.String(required=True, description="table name")
    width = graphene.Int(required=True)
    height = graphene.Int(required=True)
    capacity = graphene.Int(required=True)
    point = graphene.InputField(
        PointInput, required=True, description="position of table in canvas"
    )


class UpdateCafeTableInput(graphene.InputObjectType):
    name = graphene.String(required=True, description="table name")
    width = graphene.Int(required=True)
    height = graphene.Int(required=True)
    capacity = graphene.Int(required=True)


class CafeAdminInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    owner_id = graphene.Int(
        description="owner_id is required when sysadmin wants to create cafe. if your authorization token own cafe role, you don't need to fill this."
    )
    address = AddressInput(required=True)
    smoking_free = SmokingFreeEnum(required=True)
    # cafe_canvas = CafeCanvasInput(required=True)


class UpdateCafeAdminInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    address = AddressInput(required=True)
    smoking_free = SmokingFreeEnum(required=True)
    # cafe_canvas = CafeCanvasInput(required=True)


class PointType(DjangoObjectType):
    class Meta:
        model = Point


class CafeCanvasType(DjangoObjectType):
    id = graphene.Int(required=True)
    height = graphene.Int()
    width = graphene.Int()
    line_points = graphene.List(PointType)
    cafe = graphene.Field("graph.cafes.types.CafeType")

    class Meta:
        model = CafeCanvas

    @classmethod
    def resolve_cafe(cls, obj, info, **data):
        return obj.cafe.first()

    @classmethod
    def resolve_line_points(cls, obj, info, **data):
        return obj.points.all()


class CafeType(DjangoObjectType):
    address = graphene.Field(AddressType)
    cafe_canvas = graphene.Field(CafeCanvasType)

    class Meta:
        model = Cafe


class CafeTableType(DjangoObjectType):
    cafe = graphene.Field(CafeType)

    class Meta:
        model = CafeTable

    @classmethod
    def resolve_cafe(cls, obj, info, **data):
        return obj.canvas


class MenuInput(graphene.InputObjectType):
    name = graphene.String(required=True, description="name of menu")
    image = graphene.Field(Image, size=graphene.Int(description="Size of the image."))


class MenuType(DjangoObjectType):
    class Meta:
        model = Menu


class MenuItemInput(graphene.InputObjectType):
    fa_name = graphene.String(required=True, description="name of menu item")
    en_name = graphene.String(required=True, description="name of menu item")
    image = graphene.Field(Image, size=graphene.Int(description="Size of the image."))
    menu_item_id = graphene.ID(
        required=True, description="id of menu to be added this item"
    )


class MenuItemType(DjangoObjectType):
    class Meta:
        model = MenuItem


class MenuItemImage(graphene.ObjectType):
    id = graphene.ID(required=True, description="The ID of the image.")
    alt = graphene.String(description="The alt text of the image.")
    sort_order = graphene.Int(
        required=False,
        description=(
            "The new relative sorting position of the item (from -inf to +inf). "
            "1 moves the item one position forward, -1 moves the item one position "
            "backward, 0 leaves the item unchanged."
        ),
    )
    url = graphene.String(
        required=True,
        description="The URL of the image.",
        size=graphene.Int(description="Size of the image."),
    )

    class Meta:
        description = "Represents a menu item image."

    @staticmethod
    def resolve_id(root: Media, info):
        return graphene.Node.to_global_id("MenuItemImage", root.id)

    @staticmethod
    def resolve_url(root: Media, info, *, size=None):
        if size:
            url = get_thumbnail(root.image, size, method="thumbnail")
        else:
            url = root.image.url
        return info.context.build_absolute_uri(url)
