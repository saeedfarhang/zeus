import graphene
from cafe import error_codes
from location import error_codes as location_error_codes

CafeCanvasErrorCode = graphene.Enum.from_enum(error_codes.CafeCanvasErrorCode)

CafeErrorCode = graphene.Enum.from_enum(error_codes.CafeErrorCode)

ProvinceErrorCode = graphene.Enum.from_enum(location_error_codes.ProvinceErrorCode)

CityErrorCode = graphene.Enum.from_enum(location_error_codes.CityErrorCode)
