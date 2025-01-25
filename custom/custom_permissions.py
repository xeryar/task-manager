import re

from django.forms import model_to_dict
from rest_framework.permissions import BasePermission

from apps.user.models.role_permission_models import Resource, RolePermission


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        request_user = request.user
        user_role = request_user.role
        request_method = request.method.lower()
        request_path = request.path.replace("/api", "")

        if not request_user.is_authenticated:
            return False

        if request_user.is_superuser:
            return True

        return validate_resources(request_method, request_path, user_role)


def validate_resources(request_method, request_path, user_role):
    regex_pattern = string_url_to_regex(request_path)

    try:
        resource_dict = model_to_dict(Resource.objects.get(regex__exact=regex_pattern, method=request_method))
        resource_permission = resource_dict["permission"]
    except:
        print(f"No Resource ({request_method} => {request_path}) found on server.")
        return False

    try:
        RolePermission.objects.get(role_id=user_role, permission=resource_permission)
    except:
        print(f"RoleIDs ({user_role}) is un-authorized for ({request_method} => {request_path}) request.")
        return False

    return True


def string_url_to_regex(string_url):
    escaped_string = re.escape(string_url)
    regex_pattern = re.sub(r"\/[0-9]+\/", r"\/[0-9]+\/", escaped_string)
    regex_pattern = f"^{regex_pattern}$"
    regex_pattern = regex_pattern.replace("\\", "")
    return regex_pattern
