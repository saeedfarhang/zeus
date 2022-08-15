from accounts.models import Role, User
from ..core.federation.entities import federated_entity
from graphene_django import DjangoObjectType
from django.conf import settings

# User = settings.AUTH_USER_MODEL

@federated_entity("id")
@federated_entity("email")
class UserType(DjangoObjectType):
    class Meta:
        model = User

class UserRoleType(DjangoObjectType):
    class Meta:
        model = Role
    