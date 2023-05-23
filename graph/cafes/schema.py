import graphene
from django.db.models import Q
from graphql.error import GraphQLError
from cafe.models.cafe import Cafe
from cafe.models.cafe_map import CafeCanvas
from .types import CafeCanvasType, CafeType
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist


class CafeQueries(graphene.ObjectType):
    cafes = graphene.List(CafeType)
    cafe = graphene.Field(CafeType, id=graphene.Argument(graphene.ID, required=True))
    cafe_canvases = graphene.List(CafeCanvasType)
    cafe_for_admin = graphene.List(CafeType)

    @classmethod
    def resolve_cafe_for_admin(cls, root, info, *, id=None):
        try:
            return info.context.user.cafe.all().distinct()
        except ObjectDoesNotExist:
            raise Exception(ObjectDoesNotExist)

    @classmethod
    def resolve_cafe(cls, root, info, *, id=None, **kwargs):
        try:
            return Cafe.objects.filter(id=id).first()
        except:
            raise GraphQLError("cafes not found")

    @classmethod
    def resolve_cafes(cls, root, info, **kwargs):
        try:
            return Cafe.objects.filter()
        except:
            raise GraphQLError("cafes not found")

    @classmethod
    def resolve_cafe_canvases(cls, root, info, **kwargs):
        try:
            return CafeCanvas.objects.filter(cafe__isnull=False)
        except:
            raise GraphQLError("cafe_canvases not found")
