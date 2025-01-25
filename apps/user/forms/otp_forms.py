from django import forms
from django.core.exceptions import ValidationError

from apps.user.helpers.user_helper_functions import send_otp_via_thread, set_user_otp
from apps.user.models.user_models import UserProfile


class OTPVerificationForm(forms.Form):
    email = forms.EmailField(required=True, label="Email")
    otp = forms.CharField(max_length=6, required=True, label="OTP")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        otp = cleaned_data.get("otp")

        try:
            user = UserProfile.objects.get(email=email)
            self.user = user
        except UserProfile.DoesNotExist:
            raise ValidationError({"email": "No user found with this email."})  # type: ignore

        if self.user.is_verified:
            raise ValidationError({"email": "This user is already verified."})  # type: ignore

        if self.user.is_otp_expired:
            raise ValidationError({"otp": "The OTP has expired. Please request a new OTP."})  # type: ignore

        if self.user.otp != otp:
            raise ValidationError({"otp": "The OTP is invalid."})  # type: ignore

        return cleaned_data

    def save(self):
        if not self.user:
            raise ValidationError("Cannot save without validating the form.")

        self.user.is_verified = True
        self.user.save()


class ResendOTPForm(forms.Form):
    email = forms.EmailField(required=True, label="Email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")

        try:
            user = UserProfile.objects.get(email=email)
            self.user = user
        except UserProfile.DoesNotExist:
            raise forms.ValidationError({"email": "No user found with this email."})  # type: ignore

        if self.user.is_verified:
            raise forms.ValidationError({"email": "This user is already verified."})  # type: ignore

        if not self.user.is_otp_expired:
            raise forms.ValidationError("The OTP is still valid. Please check your email.")  # type: ignore

        return cleaned_data

    def save(self):
        if not self.user:
            raise forms.ValidationError("Cannot resend OTP without a valid user.")

        self.user = set_user_otp(self.user)
        self.user.save()
        send_otp_via_thread(self.user)
