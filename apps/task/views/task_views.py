from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.task.forms.task_forms import ProjectForm, TaskForm
from apps.task.models.task_models import Project, Task
from apps.task.serializers.task_serializers import ProjectSerializer, TaskSerializer


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    http_method_names = ["get", "post", "put", "delete"]

    def create(self, request, *args, **kwargs):
        form = ProjectForm(request.data)
        if form.is_valid():
            project = form.save()
            serializer = self.get_serializer(project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

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

    def create(self, request, *args, **kwargs):
        form = TaskForm(request.data)
        if form.is_valid():
            task = form.save()
            serializer = self.get_serializer(task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        form = TaskForm(request.data, instance=instance)
        if form.is_valid():
            task = form.save()
            serializer = self.get_serializer(task)
            return Response(serializer.data)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
