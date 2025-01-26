from django.urls import include, path

urlpatterns = [
    path("", include("apps.user.urls")),
    path("", include("apps.task.urls")),
]
