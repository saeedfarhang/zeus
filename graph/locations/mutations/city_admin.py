from core.mutations.model_mutation import ModelMutation
from graph.core.types.common import CityError
from graph.locations.types import CityInput, CityType
from location.models import City, Province


class CreateCityAdmin(ModelMutation):
    class Arguments:
        input = CityInput(required=True)

    class Meta:
        description = "create city by admin"
        model = City
        object_type = CityType
        error_type_class = CityError
        permissions = ["sysadmin"]

    @classmethod
    def perform_mutation(cls, root, info, **data):
        cleaned_input = cls.get_input(data)
        province = Province.objects.get(id=cleaned_input["province_id"])
        cleaned_input["province"] = province

        instance = super().get_instance(info, **data)
        instance = super().construct_instance(instance, cleaned_input)
        super().save(info, instance, data)

        return cls.success_response(instance)
