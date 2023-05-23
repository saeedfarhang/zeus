from django.utils.functional import SimpleLazyObject
from django.urls import reverse

from graph.cafes.mutations.cafe_map_admin import (
    AddCafeTable,
    CafeCanvasUpdate,
    RemoveCafeTable,
)
from graph.cafes.mutations.cafe_menu_admin import (
    CreateMenuAdmin,
    DeleteMenuAdmin,
    UpdateMenuAdmin,
)
from graph.locations.mutations.city_admin import (
    CreateCityAdmin,
    DeleteCityAdmin,
    UpdateCityAdmin,
)
from graph.locations.mutations.province_admin import (
    CreateProvinceAdmin,
    DeleteProvinceAdmin,
    UpdateProvinceAdmin,
)
from graph.locations.schema import LocationQueries

from .cafes.mutations.cafe_admin import (
    CreateCafeAdmin,
    DeleteCafeAdmin,
    UpdateCafeAdmin,
)

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
    update_cafe = UpdateCafeAdmin.Field()
    delete_cafe = DeleteCafeAdmin.Field()
    update_cafe_canvas = CafeCanvasUpdate.Field()

    add_cafe_table = AddCafeTable.Field()
    remove_cafe_table = RemoveCafeTable.Field()
    update_cafe_table = RemoveCafeTable.Field()

    # cafe_menu admin
    create_menu = CreateMenuAdmin.Field()
    update_menu = UpdateMenuAdmin.Field()
    delete_menu = DeleteMenuAdmin.Field()

    # location_admin
    create_province = CreateProvinceAdmin.Field()
    update_province = UpdateProvinceAdmin.Field()
    delete_province = DeleteProvinceAdmin.Field()

    create_city = CreateCityAdmin.Field()
    update_city = UpdateCityAdmin.Field()
    delete_city = DeleteCityAdmin.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
