from django.db import models
from constants import SmokingFreeStatus
from core.models.abstract_base_model import AbstractBaseModel
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Cafe(AbstractBaseModel):
    name = models.CharField(max_length=225)
    owner = models.ForeignKey(User, related_name="cafe", on_delete=models.PROTECT)
    address = models.ForeignKey(
        "location.Address",
        related_name="cafes",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    smoking_free = models.CharField(
        max_length=100, choices=SmokingFreeStatus.choices, default=SmokingFreeStatus.NO
    )

    cafe_canvas = models.ForeignKey(
        "cafe.CafeCanvas", related_name="cafe", on_delete=models.PROTECT
    )

    def __str__(self):
        return f"{self.name} [{self.id}]"
