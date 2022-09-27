import graphene
from graphql.error import GraphQLError
from cafe.models.cafe import Cafe
from core.mutations.model_mutation import ModelMutation
from graph.cafes.utils import create_address
from graph.core.types.common import CafeError
from ..types import CafeAdminInput, CafeType
from django.conf import settings

User = settings.AUTH_USER_MODEL


class CreateCafeAdmin(ModelMutation):
    class Arguments:
        input = CafeAdminInput(required=True)

    class Meta:
        description = ("create cafe.",)
        model = Cafe
        object_type = CafeType
        error_type_class = CafeError
        permissions = ["sysadmin"]
        # error_type_field = "cafe_errors"

    @classmethod
    def perform_mutation(cls, root, info, **data):
        instance = cls.get_instance(info, **data)

        cleaned_input = cls.get_input(data)
        cafe_address = cleaned_input.get("address")
        print(cafe_address)
        address = create_address(cafe_address)
        instance.address = address
        instance = cleaned_input

        # create address
        return super().perform_mutation(root, info, **data)

    # cafe = graphene.Field(CafeType)

    # class Arguments:
    #     name = graphene.String()
    #     address = AddressInput(required=True)

    # def mutate(parent, info, name, address):
    #     user = info.context.user
    #     print(user)
    #     if not user.is_authenticated or user.role.role != "sysadmin":
    #         raise GraphQLError("you can't preform this action")
    #     # try:
    #     cafe = Cafe.objects.create(name=name, owner=user)
    #     return CreateCafeAdmin(cafe=cafe)
    #     # except:
    #     # raise GraphQLError("there is a prov")
