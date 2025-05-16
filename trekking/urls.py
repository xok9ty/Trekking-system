from django.urls import path
from .views import TaskListView, TaskDetailView, TaskCreateView, CommentCreateView

app_name = 'tasks'

urlpatterns = [
    path('', TaskListView.as_view(), name='task-list'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('<int:pk>/comment/', CommentCreateView.as_view(), name='comment-create'),
]