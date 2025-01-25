import datetime

from django.http import JsonResponse
from django.utils.timezone import now
from rest_framework_simplejwt.authentication import JWTAuthentication


class RoleAccessMiddleware:
    """
    Middleware to check if the user has a role and enforce access time for 'user' roles.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            auth_result = JWTAuthentication().authenticate(request)
        except Exception:
            auth_result = None

        if auth_result is not None:
            user, token = auth_result

            user_role = user.role
            if not user_role:
                return JsonResponse({"error": "User Role is not assigned yet. Please contact the administrator."}, status=403)
            if user_role.name.lower() == "user":
                current_time = now().time()
                start_time = datetime.time(15, 0)
                end_time = datetime.time(23, 59)

                if not (start_time <= current_time <= end_time):
                    return JsonResponse({"error": "Access denied. Please access the system during allowed hours."}, status=403)

        return self.get_response(request)
