from django.shortcuts import render
from .models import Task, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .forms import TaskForm, CommentForm, TaskFilterForm
from django.contrib.auth.mixins import LoginRequiredMixin

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
        context['comment_form'] = CommentForm() 
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
    template_name = 'task_detail.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.task_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tasks:task-detail', kwargs={'pk': self.kwargs['pk']})
    

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('tasks:task-list')
    
    def get_queryset(self):
        return super().get_queryset().filter(creator=self.request.user)
    
    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
    
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('tasks:task-list')
    
    def get_queryset(self):
        return super().get_queryset().filter(creator=self.request.user)
    
class TaskListView(ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')
        
        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TaskFilterForm(self.request.GET or None)
        return context