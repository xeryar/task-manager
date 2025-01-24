from django.urls import path

from apps.user.views.auth_views import RegisterApiView

urlpatterns = [
    path("register/", RegisterApiView.as_view(), name="register"),
]
