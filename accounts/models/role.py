from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL

active_roles = (
    ("customer", "customer"),
    ("cafe", "cafe"),
    ("sysadmin", "sysadmin")
)

class Role(models.Model):
    user = models.OneToOneField(User, related_name='role',on_delete=models.PROTECT)
    role = models.CharField(max_length=120, choices=active_roles, default="customer")

    @receiver(post_save, sender=User)
    def create_user_role(sender, instance, created, **kwargs):
        if created:
            Role.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_role(sender, instance, **kwargs):
        instance.role.save()

    def __str__(self) -> str:
        return f"{self.role} [{self.user.id}]"