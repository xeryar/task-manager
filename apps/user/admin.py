from django.contrib import admin

from apps.user.models.role_permission_models import Permission, Role, RolePermission
from apps.user.models.user_models import UserProfile

admin.site.register(UserProfile)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(RolePermission)
