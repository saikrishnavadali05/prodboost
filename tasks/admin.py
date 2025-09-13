from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "priority",
        "completed_steps",
        "total_steps",
        "progress",
        "due_date",
        "created_at",
    )
    list_filter = ("status", "priority", "due_date", "created_at")
    search_fields = ("title", "description")
    ordering = ("priority", "due_date")

    def progress(self, obj):
        if obj.total_steps > 0:
            return f"{(obj.completed_steps / obj.total_steps) * 100:.1f}%"
        return "0%"
    progress.short_description = "Progress"
