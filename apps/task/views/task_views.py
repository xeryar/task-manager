from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.task.forms.task_forms import ProjectForm, TaskForm
from apps.task.models.task_models import Project, Task
from apps.task.serializers.task_serializers import ProjectSerializer, TaskSerializer
from utils.response_utils import make_forbidden_response


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    http_method_names = ["get", "post", "put", "delete"]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        form = ProjectForm(request.data)
        if form.is_valid():
            project = form.save()
            serializer = self.get_serializer(project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        form = ProjectForm(request.data, instance=instance)
        if form.is_valid():
            project = form.save()
            serializer = self.get_serializer(project)
            return Response(serializer.data)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    http_method_names = ["get", "post", "put", "delete"]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        request_user = request.user
        request_user_role = request_user.role.name.lower()

        form = TaskForm(request.data, initial={"user_role": request_user_role})
        if form.is_valid():
            task = form.save()
            serializer = self.get_serializer(task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        request_data = request.data
        instance = self.get_object()
        request_user = request.user
        request_user_role = request_user.role.name.lower()

        if request_data.get("status") == "completed" and request_user_role != "manager":
            return make_forbidden_response(message="You do not have permission to mark a task as completed.")
        if request_data.get("assigned_to") and request_user_role not in ["admin", "manager"]:
            return make_forbidden_response(message="You do not have permission to assign a task to a user.")
        if instance.assigned_to and request_user_role not in ["admin", "manager"] and instance.assigned_to != request_user:
            return make_forbidden_response(message="You do not have permission to update this task.")

        form = TaskForm(request.data, instance=instance)
        if form.is_valid():
            task = form.save()
            serializer = self.get_serializer(task)
            return Response(serializer.data)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
