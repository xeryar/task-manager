import json

from django.db.models import Q
from rest_framework import filters


class TaskFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        title = request.query_params.get("title")
        due_date = request.query_params.get("due_date")
        priorities = request.query_params.get("priorities")
        statuses = request.query_params.get("statuses")
        projects = request.query_params.get("projects")
        get_unassigned_tasks = request.query_params.get("get_unassigned_tasks")
        assigned_to_ids = request.query_params.get("assigned_to_ids")
        is_pending_approval = request.query_params.get("is_pending_approval")

        q_filter = Q()

        if title:
            title = str(title)
            q_filter &= Q(title__icontains=title)

        if due_date:
            due_date = str(due_date)
            q_filter &= Q(due_date__date=due_date)

        if priorities:
            priorities = json.loads(priorities)
            priorities = [str(priority) for priority in priorities]
            q_filter &= Q(priority__in=priorities)

        if statuses:
            statuses = json.loads(statuses)
            statuses = [str(status) for status in statuses]
            q_filter &= Q(status__in=statuses)

        if projects:
            projects = json.loads(projects)
            projects = [int(project) for project in projects]
            q_filter &= Q(project__in=projects)

        if is_pending_approval:
            is_pending_approval = bool(is_pending_approval)
            if is_pending_approval:
                q_filter &= Q(is_pending_approval=True)

        if get_unassigned_tasks:
            get_unassigned_tasks = bool(get_unassigned_tasks)
            if get_unassigned_tasks:
                q_filter &= Q(assigned_to_id__isnull=True)

        if assigned_to_ids:
            assigned_to_ids = json.loads(assigned_to_ids)
            assigned_to_ids = [int(assigned_to_id) for assigned_to_id in assigned_to_ids]
            q_filter &= Q(assigned_to_id__in=assigned_to_ids)

        return queryset.filter(q_filter).distinct()
