import graphene
from graphql.error import GraphQLError
from accounts.models.user import User
from cafe.models.cafe import Cafe
from core.mutations.model_mutation import ModelMutation
from graph.cafes.utils import create_address
from graph.core.types.common import CafeError
from ..types import CafeAdminInput, CafeType


class CreateCafeAdmin(ModelMutation):
    class Arguments:
        input = CafeAdminInput(required=True)

    class Meta:
        description = ("create cafe.",)
        model = Cafe
        object_type = CafeType
        error_type_class = CafeError
        permissions = ["sysadmin", "cafe"]
        # error_type_field = "cafe_errors"

    @classmethod
    def perform_mutation(cls, root, info, **data):
        instance = cls.get_instance(info, **data)

        cleaned_input = cls.get_input(data)
        cafe_address = cleaned_input.get("address")
        address = create_address(cafe_address)
        cleaned_input.pop("address")
        if info.context.user.role.role == "cafe":
            cafe_owner = info.context.user
        else:
            cafe_owner = User.objects.get(id=cleaned_input["owner_id"])
        cleaned_input.pop("owner_id")
        instance = super().construct_instance(instance, cleaned_input)
        instance.owner = cafe_owner
        instance.address = address

        # create address
        super().save(info, instance, data)
        return super().success_response(instance)

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
