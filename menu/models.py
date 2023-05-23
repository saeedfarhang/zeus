from django.db import models
from core.models import AbstractBaseModel


class Menu(AbstractBaseModel):
    cafe = models.ForeignKey(
        "cafe.Cafe", related_name="menus", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="menus/menu-groups", blank=True, null=True)


class MenuItem(AbstractBaseModel):
    fa_name = models.CharField(max_length=200)
    en_name = models.CharField(max_length=200)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="menus")
    image = models.ImageField(upload_to="menus/menu-items", blank=True, null=True)
