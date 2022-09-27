from location.models import City, Province


def get_all_provinces():
    return Province.objects.all()


def get_province_cities(province_id):
    return City.objects.filter(province_id=province_id)
