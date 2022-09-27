import graphene

from graph.locations.types import CityType, ProvinceType
from graph.locations.utils import get_all_provinces, get_province_cities


class LocationQueries(graphene.ObjectType):
    provinces = graphene.List(ProvinceType)
    cities = graphene.List(
        CityType,
        description="resolve province cities.",
        province_id=graphene.Argument(graphene.Int, description="province_id"),
    )

    @staticmethod
    def resolve_provinces(root, info):
        qs = get_all_provinces()
        print(qs)
        return qs

    @staticmethod
    def resolve_cities(root, info, province_id):
        qs = get_province_cities(province_id)
        print(qs)
        return qs
