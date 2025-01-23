from django.db import models

from core.models import BaseModel


class Permission(BaseModel):
    """
    Permission model to store the permissions for the roles

    id (PK): AutoField
    name: CharField
    context_value: CharField
    """

    name = models.CharField(max_length=255)
    context_value = models.CharField(max_length=255)

    class Meta:
        app_label = "user"


class Role(BaseModel):
    """
    Role model to store the roles for the users

    id (PK): AutoField
    name: CharField
    slug: SlugField

    permissions: ManyToManyField (Permission)
    """

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, null=True, unique=True)

    permissions = models.ManyToManyField(Permission, blank=True, through="RolePermission")

    class Meta:
        app_label = "user"


class Resource(BaseModel):
    """
    Resource model to store the resources for the permissions

    permission: FK (Permission)

    id (PK): AutoField
    name: CharField
    regex: CharField
    method: CharField
    """

    permission = models.ForeignKey(Permission, on_delete=models.PROTECT, null=True, blank=True, related_name="permission_resources")

    name = models.CharField(max_length=255)
    regex = models.CharField(max_length=255)
    method = models.CharField(max_length=255)

    class Meta:
        app_label = "user"


# ---------------------------------------------------------------------------- #
#                                     MAPS                                     #
# ---------------------------------------------------------------------------- #
class RolePermission(BaseModel):
    """
    RolePermission model to store the mapping between roles and permissions

    role: FK (Role)

    id (PK): AutoField
    role: FK (Role)
    permission: FK (Permission)
    """

    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    permission = models.ForeignKey(Permission, on_delete=models.PROTECT)

    class Meta:
        app_label = "user"
        db_table = "user_role_permission"
