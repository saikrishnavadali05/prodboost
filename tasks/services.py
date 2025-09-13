from django.db import transaction
from .models import Task

def progress_percent(task: Task) -> int:
    if task.total_steps == 0:
        return 0
    return int((task.completed_steps / task.total_steps) * 100)

@transaction.atomic
def set_completed_steps(task: Task, completed: int) -> Task:
    completed = max(0, min(completed, task.total_steps))
    task.completed_steps = completed
    if completed >= task.total_steps:
        task.status = 'done'
    elif completed > 0:
        task.status = 'in_progress'
    else:
        task.status = 'todo'
    task.save()
    return task

@transaction.atomic
def increment_steps(task: Task, steps: int = 1) -> Task:
    return set_completed_steps(task, task.completed_steps + steps)

@transaction.atomic
def create_task(**kwargs) -> Task:
    # Validation / defaults can be centralized here
    if kwargs.get('total_steps', 1) <= 0:
        kwargs['total_steps'] = 1
    return Task.objects.create(**kwargs)
