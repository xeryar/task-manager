from typing import Any

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel


class CustomUserManager(UserManager):
    """
    Custom user manager where email is the unique identifier, inherited from UserManager provided by auth
    """

    def create_superuser(
        self,
        email: str,
        password: str | None,
        **extra_fields: Any,
    ) -> Any:
        username = email
        return super().create_superuser(username, email, password, **extra_fields)


class UserProfile(BaseModel, AbstractUser):
    """
    User profile model where email is the unique identifier, inherited from abstract user provided by auth

    role: FK (Role)

    id (PK): AutoField
    username: CharField
    email: EmailField
    first_name: CharField
    last_name: CharField
    password: CharField
    otp: CharField
    otp_expiry: DateTimeField
    date_joined: DateTimeField
    last_login: DateTimeField

    is_verified: BooleanField
    """

    role = models.ForeignKey("user.Role", on_delete=models.PROTECT, null=True, blank=True, related_name="user_roles")

    username = models.CharField(_("username"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    password = models.CharField(_("password"), max_length=128, blank=True)
    otp = models.CharField(_("otp"), max_length=6, blank=True)
    otp_expiry = models.DateTimeField(_("otp expiry"), blank=True, null=True)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    last_login = models.DateTimeField(_("last login"), blank=True, null=True)

    is_verified = models.BooleanField(_("verified"), default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    class Meta:
        app_label = "user"

    def __str__(self):
        return self.email
