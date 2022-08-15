import graphene
from graphene_django import DjangoObjectType
from cafe.models import Cafe


class CafeType(DjangoObjectType):
    class Meta:
        model = Cafe