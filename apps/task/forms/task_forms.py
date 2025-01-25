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

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Project.objects.filter(name=name).exists():
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
            "description",
        ]

    def clean_due_date(self):
        due_date = self.cleaned_data.get("due_date")
        if due_date and convert_any_datetime_to_utc(due_date) < get_current_utc_datetime():
            raise forms.ValidationError("The due date cannot be in the past.")
        return due_date
