
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','total_steps','priority','due_date']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type':'datetime-local'})
        }
