from django.urls import path

from apps.user.views.auth_views import (
    LoginApiView,
    LogoutApiView,
    RegisterApiView,
    TokenRefreshApiView,
)

urlpatterns = [
    path("register/", RegisterApiView.as_view(), name="register"),
    path("login/", LoginApiView.as_view(), name="login"),
    path("logout/", LogoutApiView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshApiView.as_view(), name="token_refresh"),
]
