from location.models import Address


def create_address(address_input):
    instance = Address.objects.create(**address_input)
    return instance
