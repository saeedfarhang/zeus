from accounts.models import Role, User
from ..core.federation.entities import federated_entity
from graphene_django import DjangoObjectType
from django.conf import settings
import graphene
from graphql.error import GraphQLError
# User = settings.AUTH_USER_MODEL

@federated_entity("id")
@federated_entity("email")
class UserType(DjangoObjectType):
    role = graphene.String()
    class Meta:
        model = User
    
    @staticmethod
    def resolve_role(root, info, **data):
        try:
            return root.role.role
        except:
            raise GraphQLError(message="there was a problem authorizing the user.")
            
class UserRoleType(DjangoObjectType):
    class Meta:
        model = Role
    