from typing import Union
from django.db import models
from django.contrib.auth.models import PermissionsMixin, BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from versatileimagefield.fields import VersatileImageField
from django.utils.crypto import get_random_string
from django.utils import timezone

from .role import Role


class UserManager(BaseUserManager):
    def create_user(
        self, email, password=None, is_staff=False, is_active=True, **extra_fields
    ):
        """Create a user instance with the given email and password."""
        email = UserManager.normalize_email(email)
        # Google OAuth2 backend send unnecessary username field
        extra_fields.pop("username", None)

        user = self.model(
            email=email, is_active=is_active, is_staff=is_staff, **extra_fields
        )
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(
            email, password, is_staff=True, is_superuser=True, **extra_fields
        )
        role = Role.objects.get(user=user.id)
        role.role = 'sysadmin'
        role.save()
        return user
        
    def staff(self):
        return self.get_queryset().filter(is_staff=True)


class User (PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=254)
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    note = models.TextField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    avatar = VersatileImageField(upload_to="user-avatars", blank=True, null=True)
    jwt_token_key = models.CharField(max_length=12, default=get_random_string)
    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return f"{self.email} [{self.id}]"

    def get_full_name(self):
        if self.first_name or self.last_name:
            return ("%s %s" % (self.first_name, self.last_name)).strip()
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None) -> bool:
        return True

    def has_perms(
        self, perm_list, obj=None
    ) -> bool:
        # This method is overridden to accept perm as BasePermissionEnum
        # perm_list = [
        #     perm.value if isinstance(perm, BasePermissionEnum) else perm
        #     for perm in perm_list
        # ]
        # return super().has_perms(perm_list, obj)
        return True



