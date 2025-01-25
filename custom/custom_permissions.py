from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        request_user = request.user

        if not request_user.is_authenticated:
            return False

        if request_user.is_superuser:
            return True

        return True
