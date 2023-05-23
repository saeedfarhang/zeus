from core.mutations.model_mutation import ModelMutation
from graph.locations.types import ProvinceInput, ProvinceType
from location.models import Province
from graph.core.types.common import ProvinceError
import graphene


class CreateProvinceAdmin(ModelMutation):
    class Arguments:
        input = ProvinceInput(required=True)

    class Meta:
        description = "create province by admin"
        model = Province
        object_type = ProvinceType
        error_type_class = ProvinceError
        permissions = ["sysadmin"]


class UpdateProvinceAdmin(CreateProvinceAdmin):
    class Arguments:
        id = graphene.ID(required=True, description="id of province to be updated")
        input = ProvinceInput(required=True)

    class Meta:
        description = "update province by admin"
        model = Province
        object_type = ProvinceType
        error_type_class = ProvinceError
        permissions = ["sysadmin"]


class DeleteProvinceAdmin(CreateProvinceAdmin):
    class Arguments:
        id = graphene.ID(required=True, description="id of province to be deleted")

    class Meta:
        description = "delete province by admin"
        model = Province
        object_type = ProvinceType
        error_type_class = ProvinceError
        permissions = ["sysadmin"]

    @classmethod
    def perform_mutation(cls, root, info, **data):
        instance = cls.get_instance(info, **data)
        instance.delete()
        return super().delete_response()
