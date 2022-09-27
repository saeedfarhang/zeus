import graphene
from django.db.models import Q
from graphql.error import GraphQLError
from cafe.models.cafe import Cafe
from .types import CafeType


class CafeQueries(graphene.ObjectType):
    cafes = graphene.List(CafeType)
    cafe = graphene.Field(CafeType, id=graphene.Argument(graphene.ID, required=True))

    @staticmethod
    def resolve_cafe(root, info, *, id=None, **kwargs):
        try:
            return Cafe.objects.filter(id=id).first()
        except:
            raise GraphQLError("cafes not found")

    @staticmethod
    def resolve_cafes(root, info, **kwargs):
        try:
            return Cafe.objects.filter()
        except:
            raise GraphQLError("cafes not found")
