import graphene
from graphql.error import GraphQLError
from accounts.models.user import User
from cafe.models.cafe import Cafe
from core.mutations.model_mutation import ModelMutation
from graph.cafes.utils import create_address
from graph.core.types.common import CafeError
from ..types import CafeAdminInput, CafeType, UpdateCafeAdminInput
from django.core.exceptions import ValidationError


class CreateCafeAdmin(ModelMutation):
    class Arguments:
        input = CafeAdminInput(required=True)

    class Meta:
        description = ("create cafe.",)
        model = Cafe
        object_type = CafeType
        error_type_class = CafeError
        permissions = ["sysadmin", "cafe"]

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


class UpdateCafeAdmin(CreateCafeAdmin):
    @classmethod
    def instance_owner(cls, instance):
        if instance.owner_id:
            return instance.owner_id
        else:
            raise GraphQLError("cafe does not exists")

    class Arguments:
        id = graphene.ID(required=True, description="id of cafe to be updated.")
        input = UpdateCafeAdminInput(
            required=True, description="Fields required to update cafe"
        )

    class Meta:
        description = ("update a cafe.",)
        model = Cafe
        object_type = CafeType
        error_type_class = CafeError
        permissions = ["sysadmin", "cafe"]

    @classmethod
    def perform_mutation(cls, root, info, **data):
        instance = cls.get_instance(info, **data)
        cleaned_input = cls.get_input(data)
        cafe_address = cleaned_input.get("address")
        address = create_address(cafe_address)
        cleaned_input.pop("address")
        instance = super().construct_instance(instance, cleaned_input)
        instance.address.delete()
        instance.address = address

        # create address
        super().save(info, instance, data)
        return super().success_response(instance)


class DeleteCafeAdmin(UpdateCafeAdmin):
    class Arguments:
        id = graphene.ID(required=True, description="id of cafe to be updated.")

    class Meta:
        description = ("delete a cafe.",)
        model = Cafe
        object_type = CafeType
        error_type_class = CafeError
        permissions = ["sysadmin", "cafe"]

    @classmethod
    def perform_mutation(cls, root, info, **data):
        instance = cls.get_instance(info, **data)
        instance.address.delete()
        instance.delete()
        return super().success_response(instance)
