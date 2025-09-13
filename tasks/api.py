# tasks/api.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny  # or IsAuthenticated if needed
from .models import Task
from .serializers import TaskSerializer
from .services import set_completed_steps, increment_steps

@api_view(['GET'])
def task_list_api(request):
    qs = Task.objects.all()
    serializer = TaskSerializer(qs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def task_detail_api(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = TaskSerializer(task)
    return Response(serializer.data)

# --- updated to handle 'reset' ---
@api_view(['POST'])
@permission_classes([AllowAny])  # temporary, can use proper auth
def task_update_progress_api(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    action = request.data.get('action')

    if action == 'set':
        value = int(request.data.get('value', 0))
        task = set_completed_steps(task, value)

    elif action == 'incr':
        step = int(request.data.get('step', 1))
        task = increment_steps(task, step)

    elif action == 'reset':
        task = set_completed_steps(task, 0)  # reset to 0

    else:
        return Response({'detail': 'unknown action'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = TaskSerializer(task)
    return Response(serializer.data)
