from django.utils.functional import SimpleLazyObject
from django.urls import reverse

from .accounts.schema import AccountQueries
from .accounts.schema import AccountQueries

# from .core.federation.schema import build_federated_schema
import graphene
import graphql_jwt

API_PATH = SimpleLazyObject(lambda: reverse("api"))

class Queries (
    AccountQueries,
    graphene.ObjectType
):
    ...

class Mutations(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    verify_token = graphql_jwt.Verify.Field()    

    ...

schema = graphene.Schema(query=Queries, mutation=Mutations)
