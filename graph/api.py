from django.utils.functional import SimpleLazyObject
from django.urls import reverse

from .cafes.schema import CafeQueries

from .accounts.mutations.users import CreateUser, LoginUser

from .accounts.schema import AccountQueries
from .accounts.schema import AccountQueries

# from .core.federation.schema import build_federated_schema
import graphene
import graphql_jwt

API_PATH = SimpleLazyObject(lambda: reverse("api"))

class Query (
    AccountQueries,
    CafeQueries,
):
    ...

class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    verify_token = graphql_jwt.Verify.Field()
    user_signup = CreateUser.Field()
    user_login = LoginUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
