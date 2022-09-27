from django.db import models
from core.models import AbstractBaseModel
from django.conf import settings

# Create your models here.

User = settings.AUTH_USER_MODEL


class Address(AbstractBaseModel):
    city = models.ForeignKey("City", on_delete=models.PROTECT, related_name="addresses")
    title = models.CharField(max_length=180)
    address = models.TextField(max_length=1000)
    phone_number = models.CharField(max_length=11)
    landline_number = models.CharField(max_length=11)
    latitude = models.DecimalField(max_digits=8, decimal_places=6, default=0)
    longitude = models.DecimalField(max_digits=8, decimal_places=6, default=0)


class City(AbstractBaseModel):
    fa_name = models.CharField(max_length=225)
    en_name = models.CharField(max_length=225, blank=True, null=True)
    province = models.ForeignKey(
        "Province", on_delete=models.CASCADE, related_name="cities"
    )
    latitude = models.DecimalField(max_digits=8, decimal_places=6, default=0)
    longitude = models.DecimalField(max_digits=8, decimal_places=6, default=0)

    class Meta:
        unique_together = ("fa_name", "en_name", "province")


class Province(AbstractBaseModel):
    fa_name = models.CharField(max_length=225)
    en_name = models.CharField(max_length=225, blank=True, null=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=6, default=0)
    longitude = models.DecimalField(max_digits=8, decimal_places=6, default=0)

    class Meta:
        unique_together = (
            "fa_name",
            "en_name",
        )
