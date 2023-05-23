# import pytest
# from .models import Cafe, CafeCanvas, CafeElement, Point


# @pytest.mark.parametrize(
#     "name, owner_id",
#     (
#         (
#             "hello",
#             1,
#         ),  # price equal min price
#         (
#             "hello",
#             2,
#         ),  # price equal min price
#         (
#             "hello friend",
#             1,
#         ),  # price equal min price
#     ),
# )  # regular case
# def test_creating_cafe_flow(name, owner_id):
#     method = shipping_zone.shipping_methods.create(
#         type=ShippingMethodType.PRICE_BASED,
#     )
#     ShippingMethodChannelListing.objects.create(
#         currency=channel_USD.currency_code,
#         minimum_order_price_amount=min_price,
#         maximum_order_price_amount=max_price,
#         shipping_method=method,
#         channel=channel_USD,
#     )
#     ShippingMethodChannelListing.objects.create(
#         currency=other_channel_USD.currency_code,
#         minimum_order_price_amount=min_price,
#         maximum_order_price_amount=max_price,
#         shipping_method=method,
#         channel=other_channel_USD,
#     )
#     assert "PL" in shipping_zone.countries
#     result = ShippingMethod.objects.applicable_shipping_methods(
#         price=Money(price, "USD"),
#         weight=Weight(kg=0),
#         country_code="PL",
#         channel_id=channel_USD.id,
#     )
#     result_ids = set([method.id for method in result])
#     assert len(result_ids) == len(result)
#     assert (method in result) == shipping_included
