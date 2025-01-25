from django.db import models

from core.models import BaseModel


class Project(BaseModel):
    """
    Project model to store project details

    id (PK): AutoField
    name: CharField
    """

    name = models.CharField(max_length=255)

    class Meta:
        app_label = "task"

    def __str__(self):
        return self.name


class Task(BaseModel):
    """
    Task model to store task details for the projects

    project: FK (Project)

    id (PK): AutoField
    title: CharField
    due_date: DateTimeField
    priority: CharField (choices: low, medium, high)
    status: CharField (choices: pending, in_progress, completed) (default: pending)
    """

    project = models.ForeignKey("task.Project", on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    due_date = models.DateTimeField()

    PRIORITY_CHOICES = [("low", "Low"), ("medium", "Medium"), ("high", "High")]
    STATUS_CHOICES = [("pending", "Pending"), ("in_progress", "In Progress"), ("completed", "Completed")]

    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default="low", blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending", blank=True)

    class Meta:
        app_label = "task"

    def __str__(self):
        return self.title
