from django.db import models
from core.models import AbstractBaseModel


class Menu(AbstractBaseModel):
    cafe = models.ForeignKey(
        "cafe.Cafe", related_name="menus", on_delete=models.CASCADE
    )
    items = models.ManyToManyField("MenuItem", related_name="menu")


class MenuItem(AbstractBaseModel):
    fa_name = models.CharField(max_length=200)
