from ..core.federation.entities import federated_entity
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model

User = get_user_model()

@federated_entity("id")
@federated_entity("email")
class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')