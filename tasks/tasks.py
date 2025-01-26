from datetime import timedelta

from django.conf import settings
from django.utils.timezone import now

from apps.task.models.task_models import Task


def delete_completed_tasks():
    deletion_period_days = getattr(settings, "TASK_DELETION_PERIOD_DAYS", 2)
    threshold_date = now() - timedelta(days=deletion_period_days)

    tasks_to_delete = Task.objects.filter(status="completed", updated_at__lt=threshold_date)
    deleted_count, _ = tasks_to_delete.delete()
    return deleted_count
