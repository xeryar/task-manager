from django.db import transaction
from rest_framework import status, views
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.user.forms.auth_forms import UserRegistrationForm
from apps.user.models.user_models import UserProfile


class RegisterApiView(views.APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.data)
        if form.is_valid():
            form.save()
            return Response(
                {
                    "message": "Success",
                    "message": "User registered successfully! Please verify your email to activate your account.",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response({"message": "Failed", "errors": form.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        request_data = request.data
        email: str = request_data.get("email")  # type: ignore
        user = UserProfile.objects.filter(email=email).first()
        if not user:
            return Response({"message": "Failed", "errors": {"email": "User not found"}}, status=status.HTTP_400_BAD_REQUEST)
        if not (user.is_superuser or user.is_verified):
            return Response({"message": "Failed", "errors": {"email": "User not verified"}}, status=status.HTTP_400_BAD_REQUEST)
        return super().post(request, *args, **kwargs)


class LogoutApiView(TokenBlacklistView):
    permission_classes = [AllowAny]

    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


class TokenRefreshApiView(TokenRefreshView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)
