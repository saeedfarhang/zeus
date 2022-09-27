from django.utils.functional import SimpleLazyObject
from django.urls import reverse

from graph.cafes.mutations.cafe_map_admin import CafeCanvasCreate
from graph.locations.mutations.city_admin import CreateCityAdmin
from graph.locations.mutations.province_admin import CreateProvinceAdmin
from graph.locations.schema import LocationQueries

from .cafes.mutations.cafe_admin import CreateCafeAdmin

from .cafes.schema import CafeQueries

from .accounts.mutations.users import CreateUser, LoginUser

from .accounts.schema import AccountQueries
from .accounts.schema import AccountQueries

# from .core.federation.schema import build_federated_schema
import graphene
import graphql_jwt

API_PATH = SimpleLazyObject(lambda: reverse("api"))


class Query(AccountQueries, CafeQueries, LocationQueries):
    ...


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    verify_token = graphql_jwt.Verify.Field()
    user_signup = CreateUser.Field()
    user_login = LoginUser.Field()
    # cafe admin
    create_cafe = CreateCafeAdmin.Field()
    create_cafe_canvas = CafeCanvasCreate.Field()
    # location_admin
    create_province = CreateProvinceAdmin.Field()
    create_city = CreateCityAdmin.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
