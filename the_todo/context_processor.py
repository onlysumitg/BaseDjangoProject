def to_do_context_processor(request):
    if request.user.is_authenticated:
        pending_tasks = request.user.todo.filter(completed=False)[:5]
        completed_tasks = request.user.todo.filter(completed=False)[:5]
        pending_task_count = request.user.todo.filter(completed=False).count()
        return {"pending_tasks": pending_tasks, "pending_task_count": pending_task_count}

    return {"pending_tasks": [], "pending_task_count": 0}
