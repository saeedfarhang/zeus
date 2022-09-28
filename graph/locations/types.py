import graphene
from graphene_django import DjangoObjectType
from location.models import Address, City, Province


class AddressInput(graphene.InputObjectType):
    title = graphene.String(description="title of address")
    city_id = graphene.Int(description="selected city id")
    address = graphene.String(description="address of place")
    phone_number = graphene.String(description="phone number start with 09")
    landline_number = graphene.String(
        description="landline number start with city code"
    )


class AddressType(DjangoObjectType):
    class Meta:
        model = Address


class ProvinceInput(graphene.InputObjectType):
    fa_name = graphene.String()
    en_name = graphene.String()
    latitude = graphene.Decimal()
    longitude = graphene.Decimal()


class ProvinceType(DjangoObjectType):
    class Meta:
        model = Province


class CityInput(graphene.InputObjectType):
    province_id = graphene.Int()
    fa_name = graphene.String()
    en_name = graphene.String()
    latitude = graphene.Decimal()
    longitude = graphene.Decimal()


class CityType(DjangoObjectType):
    class Meta:
        model = City
