from django import forms

from apps.task.models.task_models import Project, Task
from utils.datetime_utils import convert_any_datetime_to_utc, get_current_utc_datetime


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "name",
            "description",
        ]

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get("instance", None)
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Project.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A project with this name already exists.")
        return name


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "project",
            "title",
            "due_date",
            "priority",
            "status",
            "assigned_to",
            "description",
        ]

    def __init__(self, *args, **kwargs):
        self._initial = kwargs.get("initial", {})
        self.instance = kwargs.get("instance", None)
        super().__init__(*args, **kwargs)
        user_role = self._initial.get("user_role", None)
        if user_role and user_role not in ["admin", "manager"]:
            self.fields.pop("assigned_to")

    def clean_status(self):
        status = self.cleaned_data.get("status")
        if self.instance and not self.instance.pk:
            status = "pending"
        return status

    def clean(self):
        cleaned_data = super().clean()
        if self.instance and self.instance.is_completed:
            raise forms.ValidationError("You cannot update a completed task.")
        return cleaned_data

    def clean_due_date(self):
        due_date = self.cleaned_data.get("due_date")
        if self.instance and self.instance.is_completed:
            return due_date
        if due_date and convert_any_datetime_to_utc(due_date) < get_current_utc_datetime():
            raise forms.ValidationError("The due date cannot be in the past.")
        return due_date
