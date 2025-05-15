from django.shortcuts import render
from .models import Task
from django.views.generic import ListView, DetailView

# Create your views here.
class TaskListView(ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'


class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'
    
