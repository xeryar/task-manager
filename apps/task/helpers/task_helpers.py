from utils.response_utils import make_forbidden_response


def validate_task_access(request, instance):
    """
    Validate if the user has access to the task. Only admin, manager, and the assigned user can access the task.
    :param request: Request object
    :param instance: Task instance
    :return: Response object if the user does not have access to the task, else None
    """
    request_user = request.user
    request_user_role = request_user.role.name.lower()

    if request_user_role != "user" and instance.assigned_to_id != request_user.id:
        return {"response": make_forbidden_response(message="You do not have permission to modify or access this task.")}
    return None
