from django.db import models, transaction
from versatileimagefield.fields import VersatileImageField, PPOIField
from django.db.models import F
from cafe.models import MediaTypes


# Create your models here.


class Media(models.Model):
    # product = models.ForeignKey(
    #     Product, related_name="media", on_delete=models.SET_NULL, null=True, blank=True
    # )
    image = VersatileImageField(
        upload_to="media", ppoi_field="ppoi", blank=True, null=True
    )
    ppoi = PPOIField()
    alt = models.CharField(max_length=128, blank=True)
    type = models.CharField(
        max_length=32,
        choices=MediaTypes.CHOICES,
        default=MediaTypes.IMAGE,
    )
    external_url = models.CharField(max_length=256, blank=True, null=True)
    oembed_data = models.JSONField(blank=True, default=dict)
    to_remove = models.BooleanField(default=False)

    class Meta:
        ordering = ("sort_order", "pk")
        app_label = "media"

    def get_ordering_queryset(self):
        return self.all()

    @transaction.atomic
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    @transaction.atomic
    def set_to_remove(self):
        self.to_remove = True
        self.save(update_fields=["to_remove"])
        if self.sort_order is not None:
            qs = self.get_ordering_queryset()
            qs.filter(sort_order__gt=self.sort_order).update(
                sort_order=F("sort_order") - 1
            )
