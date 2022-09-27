import graphene
from graphene_django import DjangoObjectType
from cafe.models import Cafe, CafeCanvas, Point
from graph.core.types.model import ModelObjectType
from graph.locations.types import AddressInput


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
    height = graphene.Int()
    width = graphene.Int()
    line_points = graphene.List(PointInput)


class CafeAdminInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    owner_id = graphene.Int()
    address = AddressInput(required=True)
    smoking_free = SmokingFreeEnum(required=True)
    # cafe_canvas = CafeCanvasInput(required=True)


class PointType(DjangoObjectType):
    class Meta:
        model = Point


class CafeType(DjangoObjectType):
    class Meta:
        model = Cafe


class CafeCanvasType(ModelObjectType):
    id = graphene.GlobalID(required=True)
    height = graphene.Int()
    width = graphene.Int()
    line_points = graphene.List(PointType)

    class Meta:
        model = CafeCanvas
