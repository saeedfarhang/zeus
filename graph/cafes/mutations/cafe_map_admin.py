import graphene
from cafe.models import CafeCanvas

from core.mutations.model_mutation import ModelMutation
from ..types import CafeCanvasInput, CafeCanvasType
from ...core.types.common import CafeCanvasError


class CafeCanvasCreate(ModelMutation):
    class Arguments:
        input = CafeCanvasInput(required=True)

    class Meta:
        description = "create cafe canvas with line points."
        model = CafeCanvas
        object_type = CafeCanvasType
        error_type_class = CafeCanvasError
        error_type_field = "cafe_canvas_errors"

    @classmethod
    def perform_mutation(cls, root, info, **data):
        return super().perform_mutation(root, info, **data)
