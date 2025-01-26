from celery import shared_task
from django.core.cache import cache

from apps.task.models.task_models import Task


@shared_task
def save_task_to_db(task_id):
    task_data = cache.get(f"task:{task_id}")
    if task_data:
        task = Task.objects.filter(id=task_data["id"]).first()
        if task:
            task.status = task_data["status"]
            task.is_pending_approval = task_data["is_pending_approval"]
            task.save()
        cache.delete(f"task:{task_id}")
