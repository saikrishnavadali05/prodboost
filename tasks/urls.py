from django.urls import path
from . import views, api
from .views import TaskCreateView

app_name = 'tasks'

urlpatterns = [
    path('', views.TaskListView.as_view(), name='list'),
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='detail'),
     path('create/', TaskCreateView.as_view(), name='create'),

    # API
    path('api/tasks/', api.task_list_api, name='api-list'),
    path('api/tasks/<int:pk>/', api.task_detail_api, name='api-detail'),
    path('api/tasks/<int:pk>/progress/', api.task_update_progress_api, name='api-progress'),
]
