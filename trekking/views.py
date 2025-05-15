from django.shortcuts import render
from .models import Task
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .forms import TaskForm

# Create your views here.
class TaskListView(ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'


class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'
    
class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('tasks:task-list')  

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)