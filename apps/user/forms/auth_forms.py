from django import forms
from django.core.exceptions import ValidationError

from apps.user.models.user_models import UserProfile


class UserRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password", required=True)

    class Meta:
        model = UserProfile
        fields = ["email", "first_name", "last_name", "password", "confirm_password"]

    password = forms.CharField(widget=forms.PasswordInput, label="Password", required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError({"confirm_password": "Passwords do not match."})  # type: ignore

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        # user.role = Role.objects.get(slug="user")
        if commit:
            user.save()
        return user
