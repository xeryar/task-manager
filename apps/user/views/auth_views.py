from django.db import transaction
from rest_framework import views, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.user.forms.auth_forms import UserRegistrationForm
from apps.user.forms.otp_forms import OTPVerificationForm, ResendOTPForm
from apps.user.models.user_models import UserProfile
from utils.response_utils import (
    make_created_response,
    make_error_response,
    make_success_response,
)


class RegisterApiView(views.APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.data)
        if form.is_valid():
            form.save()
            return make_created_response(message="User registered successfully. Please verify your email address.")
        return make_error_response(data=form.errors)


class LoginApiView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        request_data = request.data
        email: str = request_data.get("email")  # type: ignore
        user = UserProfile.objects.filter(email=email).first()
        if not user:
            return make_error_response(message="User not found.")
        if not (user.is_superuser or user.is_verified):
            return make_error_response(message="Your account is not verified. Please verify your email address.")
        return super().post(request, *args, **kwargs)


class LogoutApiView(TokenBlacklistView):
    permission_classes = [AllowAny]

    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


class TokenRefreshApiView(TokenRefreshView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


class OTPVerificationAPIViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def verify_otp(self, request, *args, **kwargs):
        form = OTPVerificationForm(request.data)
        if form.is_valid():
            form.save()
            return make_success_response(message="OTP verified successfully.")

        return make_error_response(data=form.errors)

    def resend_otp(self, request, *args, **kwargs):
        form = ResendOTPForm(request.data)
        if form.is_valid():
            form.save()
            return make_success_response(message="OTP resent successfully.")

        return make_error_response(data=form.errors)
