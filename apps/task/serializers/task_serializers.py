from rest_framework import serializers

from apps.task.models.task_models import Project, Task
from core.serializers import BaseModelSerializer, get_base_model_fields


class ProjectSerializer(BaseModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "name",
        ] + get_base_model_fields()

        read_only_fields = [
            "id",
        ]

    def __init__(self, *args, **kwargs):
        self._context = kwargs.get("context", {})
        if self._context.get("get_tasks", False):
            self.fields["total_tasks"] = serializers.IntegerField(read_only=True)
            self.fields["pending_tasks"] = serializers.IntegerField(read_only=True)
            self.fields["in_progress_tasks"] = serializers.IntegerField(read_only=True)
            self.fields["completed_tasks"] = serializers.IntegerField(read_only=True)
            self.fields["tasks"] = TaskSerializer(many=True, read_only=True, source="project_tasks", context={"remove_project": True})
        super().__init__(*args, **kwargs)


class TaskSerializer(BaseModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "project",
            "title",
            "due_date",
            "priority",
            "status",
        ] + get_base_model_fields()

        read_only_fields = [
            "id",
        ]

    def __init__(self, *args, **kwargs):
        self._context = kwargs.get("context", {})
        if self._context.get("remove_project", False):
            self.fields.pop("project")
        if self._context.get("get_project", False):
            self.fields["project"] = ProjectSerializer(read_only=True)
        super().__init__(*args, **kwargs)
