from django.conf import settings
from django.core.management.base import BaseCommand
from django_celery_beat.models import IntervalSchedule, PeriodicTask


class Command(BaseCommand):
    help = "Create or update periodic tasks for Celery Beat"

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating/Updating periodic tasks...")
        interval_days = getattr(settings, "CELERY_TASK_DELETION_INTERVAL_DAYS", 7)

        schedule, created = IntervalSchedule.objects.get_or_create(
            every=interval_days,
            period=IntervalSchedule.DAYS,
        )

        task, task_created = PeriodicTask.objects.update_or_create(
            name="Weekly Task Deletion",
            defaults={
                "task": "tasks.scheduled_tasks.scheduled_task_deletion",
                "interval": schedule,
                "enabled": True,
            },
        )

        if created:
            self.stdout.write(self.style.SUCCESS("Interval schedule created."))
        if task_created:
            self.stdout.write(self.style.SUCCESS("Periodic task created."))
        else:
            self.stdout.write(self.style.SUCCESS("Periodic task updated."))

        self.stdout.write(self.style.SUCCESS("All periodic tasks processed successfully!"))
