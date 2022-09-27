from django.db import models
from core.models.abstract_base_model import AbstractBaseModel


class Point(models.Model):
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    canvas = models.ForeignKey(
        "CafeCanvas",
        related_name="points",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )


class CafeCanvas(AbstractBaseModel):
    # each cafe have a canvas for there plan schematic
    height = models.IntegerField(default=64)
    width = models.IntegerField(default=64)


class CafeElement(AbstractBaseModel):
    name = models.CharField(max_length=100)
    width = models.IntegerField(default=2)
    height = models.IntegerField(default=2)
    canvas = models.ForeignKey(
        CafeCanvas, related_name="element", on_delete=models.PROTECT
    )
    point = models.ForeignKey(Point, related_name="element", on_delete=models.CASCADE)
