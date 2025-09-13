from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    percent = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id','title','description','total_steps','completed_steps','percent','priority','status','due_date']

    def get_percent(self, obj):
        if obj.total_steps == 0:
            return 0
        return int((obj.completed_steps / obj.total_steps) * 100)