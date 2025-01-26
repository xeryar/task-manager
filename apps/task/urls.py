from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.task.views.task_views import ProjectViewSet, TaskViewSet

router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="project")
router.register("tasks", TaskViewSet, basename="task")

urlpatterns = []

urlpatterns += router.urls
