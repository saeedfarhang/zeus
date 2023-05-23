from os import lseek
import graphene
from graphql import GraphQLError
from cafe.models.cafe_map import CafeCanvas, CafeTable, Point
from django.core.exceptions import ObjectDoesNotExist
from core.mutations.model_mutation import ModelMutation
from ..types import (
    AddCafeTableInput,
    CafeCanvasInput,
    CafeCanvasType,
    CafeTableType,
    UpdateCafeTableInput,
)
from ...core.types.common import CafeCanvasError, CafeTableError


class CafeCanvasUpdate(ModelMutation):
    class Arguments:
        id = graphene.ID(required=True, description="id of cafe_canvas to be updated.")
        input = CafeCanvasInput(required=True)

    class Meta:
        description = ("update cafe canvas with line points.",)
        model = CafeCanvas
        object_type = CafeCanvasType
        error_type_class = CafeCanvasError
        permissions = ["sysadmin", "cafe"]

    @classmethod
    def instance_owner(cls, instance):
        if instance.cafe.first():
            return instance.cafe.first().owner_id
        else:
            raise GraphQLError("cafe canvas does not exists")

    @classmethod
    def perform_mutation(cls, root, info, **data):
        instance = cls.get_instance(info, **data)
        cleaned_input = cls.get_input(data)
        canvas_points = cleaned_input.get("line_points")
        cleaned_input.pop("line_points")
        instance.points.all().delete()
        bulk_points = []
        for point in canvas_points:
            bulk_points.append(
                Point(x=point["x"], y=point["y"], order=point["order"], canvas=instance)
            )
        instance.points.bulk_create(bulk_points)

        # create address
        super().save(info, instance, data)
        return super().success_response(instance)


class AddCafeTable(ModelMutation):
    class Arguments:
        cafe_canvas_id = graphene.ID(
            required=True, description="id of cafe canvas to be added the table."
        )
        input = AddCafeTableInput(required=True)

    class Meta:
        description = ("add cafe table to cafe canvas.",)
        model = CafeTable
        object_type = CafeTableType
        error_type_class = CafeTableError
        permissions = ["sysadmin", "cafe"]

    @classmethod
    def instance_owner(cls, instance):
        if instance.canvas.cafe.first():
            return instance.canvas.cafe.first().owner_id
        else:
            raise GraphQLError("cafe canvas does not exists")

    @classmethod
    def perform_mutation(cls, root, info, cafe_canvas_id, **data):
        cafe_canvas = CafeCanvas.objects.get(id=cafe_canvas_id)
        cleaned_input = cls.get_input(data)
        table_point = Point.objects.create(**cleaned_input["point"])
        cleaned_input.pop("point")
        instance = CafeTable(**cleaned_input, point=table_point, canvas=cafe_canvas)
        cls.check_owner(info, instance)
        instance.save()

        return cls.success_response(instance)


class RemoveCafeTable(AddCafeTable):
    class Arguments:
        id = graphene.ID(required=True, description="id of table to be deleted")

    class Meta:
        description = ("remove cafe table.",)
        model = CafeTable
        object_type = CafeTableType
        error_type_class = CafeTableError
        permissions = ["sysadmin", "cafe"]

    @classmethod
    def perform_mutation(cls, root, info, id):
        instance = CafeTable.objects.get(id=id)
        instance.point.delete()
        instance.delete()
        return cls.delete_response()


class UpdateCafeTable(AddCafeTable):
    class Arguments:
        id = graphene.ID(required=True, description="id of table to be updated")
        input = UpdateCafeTableInput(
            required=True, description="input of table to be updated"
        )

    class Meta:
        description = ("remove cafe table.",)
        model = CafeTable
        object_type = CafeTableType
        error_type_class = CafeTableError
        permissions = ["sysadmin", "cafe"]

    @classmethod
    def perform_mutation(cls, root, info, id):
        instance = CafeTable.objects.get(id=id)
        instance.point.delete()
        instance.delete()
        return cls.delete_response()
