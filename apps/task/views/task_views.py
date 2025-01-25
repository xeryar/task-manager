from django.db import transaction
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.task.filters.task_filters import TaskFilter
from apps.task.forms.task_forms import ProjectForm, TaskForm
from apps.task.helpers.task_helpers import validate_task_access
from apps.task.models.task_models import Project, Task
from apps.task.serializers.task_serializers import ProjectSerializer, TaskSerializer
from utils.response_utils import (
    make_created_response,
    make_error_response,
    make_forbidden_response,
)


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    http_method_names = ["get", "post", "put", "delete"]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == "retrieve":
            context["get_tasks"] = True
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "retrieve":
            queryset = Project.get_detailed_queryset()
        return queryset

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        form = ProjectForm(request.data)
        if form.is_valid():
            project = form.save()
            serializer = self.get_serializer(project)
            return make_created_response(data=serializer.data)
        return make_error_response(data=form.errors)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        form = ProjectForm(request.data, instance=instance)
        if form.is_valid():
            project = form.save()
            serializer = self.get_serializer(project)
            return Response(serializer.data)
        return make_error_response(data=form.errors)


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [TaskFilter, OrderingFilter]
    ordering_fields = ["id", "title", "due_date", "priority", "status"]
    ordering = ["-id"]
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "retrieve":
            queryset = queryset.select_related("project")
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == "retrieve":
            context["get_project"] = True
        return context

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        form = TaskForm(request.data)
        if form.is_valid():
            task = form.save()
            serializer = self.get_serializer(task)
            return make_created_response(data=serializer.data)
        return make_error_response(data=form.errors)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        invalid_response = validate_task_access(request, instance)
        if invalid_response:
            return invalid_response["response"]
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        request_user = request.user
        request_user_role = request_user.role.name.lower()

        if request_user_role == "user":
            queryset = self.filter_queryset(self.get_queryset())
            self.queryset = queryset.filter(assigned_to=request.user)
        return super().list(request, *args, **kwargs)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        request_data = request.data
        request_user = request.user
        request_user_role = request_user.role.name.lower()
        instance = self.get_object()
        invalid_response = validate_task_access(request, instance)
        if invalid_response:
            return invalid_response["response"]
        if request_data.get("status") == "completed" and request_user_role != "manager":
            return make_forbidden_response(message="You do not have permission to mark a task as completed.")
        form = TaskForm(request.data, instance=instance, initial={"user_role": request_user_role})
        if form.is_valid():
            task = form.save()
            serializer = self.get_serializer(task)
            return Response(serializer.data)
        return make_error_response(data=form.errors)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        invalid_response = validate_task_access(request, instance)
        if invalid_response:
            return invalid_response["response"]
        if instance.is_completed:
            return make_forbidden_response(message="You cannot delete a completed task.")
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=["post"], url_path="approvals")
    def task_approvals(self, request):
        request_data = request.data
        approved_tasks = request_data.get("approved_tasks", [])
        rejected_tasks = request_data.get("rejected_tasks", [])
        if not approved_tasks and not rejected_tasks:
            return make_error_response(message="Please provide approved_tasks or rejected_tasks.")
        if approved_tasks:
            Task.objects.filter(id__in=approved_tasks).update(is_pending_approval=False, status="completed")
        if rejected_tasks:
            Task.objects.filter(id__in=rejected_tasks).update(is_pending_approval=False)
        return make_created_response(message="Task approvals updated successfully.")
