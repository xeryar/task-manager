from django.db import transaction
from rest_framework import status, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.user.forms.auth_forms import UserRegistrationForm


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
