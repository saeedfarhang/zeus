from django.db import models
from core.models.abstract_base_model import AbstractBaseModel
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Cafe(AbstractBaseModel):
    name = models.CharField(max_length=225)
    owner = models.ForeignKey(User, related_name="cafe", on_delete=models.PROTECT)
    
    def __str__(self):
        return f"{self.name} [{self.id}]"