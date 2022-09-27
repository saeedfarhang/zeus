import graphene

from graph.core.enums import (
    CafeCanvasErrorCode,
    CafeErrorCode,
    ProvinceErrorCode,
    CityErrorCode,
)


class NonNullList(graphene.List):
    """A list type that automatically adds non-null constraint on contained items."""

    def __init__(self, of_type, *args, **kwargs):
        of_type = graphene.NonNull(of_type)
        super(NonNullList, self).__init__(of_type, *args, **kwargs)


class Error(graphene.ObjectType):
    field = graphene.String(
        description=(
            "Name of a field that caused the error. A value of `null` indicates that "
            "the error isn't associated with a particular field."
        ),
        required=False,
    )
    message = graphene.String(description="The error message.")

    class Meta:
        description = "Represents an error in the input of a mutation."


class CafeCanvasError(Error):
    code = CafeCanvasErrorCode(description="The error code.", required=True)


class CafeError(Error):
    code = CafeErrorCode(description="The error code.", required=True)


class ProvinceError(Error):
    code = ProvinceErrorCode(description="The error code.", required=True)


class CityError(Error):
    code = CityErrorCode(description="The error code.", required=True)
