from core.mutations.model_mutation import ModelMutation
from graph.locations.types import ProvinceInput, ProvinceType
from location.models import Province
from graph.core.types.common import ProvinceError


class CreateProvinceAdmin(ModelMutation):
    class Arguments:
        input = ProvinceInput(required=True)

    class Meta:
        description = "create province by admin"
        model = Province
        object_type = ProvinceType
        error_type_class = ProvinceError
        permissions = ["sysadmin"]

