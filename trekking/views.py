from django.shortcuts import render
from .models import Task, Comment
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy, reverse
from .forms import TaskForm, CommentForm

# Create your views here.
class TaskListView(ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'


class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('-created_at')
        return context
    
class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('tasks:task-list')  

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    
class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'trekking/task_detail.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.task_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tasks:task-detail', kwargs={'pk': self.kwargs['pk']})