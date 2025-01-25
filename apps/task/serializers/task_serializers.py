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
