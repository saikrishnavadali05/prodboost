# tasks/views.py
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseBadRequest
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Task
from .forms import TaskForm

# --- existing class-based views ---

class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:list')


# --- new API view for progress updates ---

@method_decorator(csrf_exempt, name="dispatch")
class TaskProgressView(View):
    def post(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return JsonResponse({"error": "Task not found"}, status=404)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")

        action = data.get("action")

        if action == "incr":
            step = int(data.get("step", 1))
            task.completed_steps = min(task.completed_steps + step, task.total_steps)

        elif action == "reset":
            task.completed_steps = 0

        else:
            return JsonResponse({"error": "Invalid action"}, status=400)

        # Update task status automatically
        if task.completed_steps >= task.total_steps:
            task.status = "done"
        elif task.completed_steps > 0:
            task.status = "in_progress"
        else:
            task.status = "todo"

        task.save()

        percent = round((task.completed_steps / task.total_steps) * 100, 2) if task.total_steps > 0 else 0

        return JsonResponse({
            "id": task.id,
            "title": task.title,
            "completed_steps": task.completed_steps,
            "total_steps": task.total_steps,
            "status": task.status,
            "percent": percent,
        })
