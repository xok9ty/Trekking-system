from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Create your models here.

class Task(models.Model):

    STATUS_CHOICES = [
        ('new', 'Нове'),
        ('in_progress', 'В роботі'),
        ('completed', 'Завершене'),
        ('archived', 'Архівоване'),
    ]
    
    PRIORITY_CHOICES = [
        (1, 'Низький'),
        (2, 'Середній'),
        (3, 'Високий'),
        (4, 'Критичний'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Назва')
    description = models.TextField(verbose_name='Опис')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2, verbose_name='Пріоритет', validators=[MinValueValidator(1), MaxValueValidator(4)])
    deadline = models.DateTimeField(verbose_name='Термін виконання', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks', verbose_name='Створив')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks', verbose_name='Відповідальний')
    
    class Meta:
        verbose_name = 'Завдання'
        verbose_name_plural = 'Завдання'
        ordering = ['-priority', 'deadline']
    
    def __str__(self):
        return self.title
    
#    @property
#    def is_overdue(self):
#        if self.deadline:
#            return timezone.now() > self.deadline
#        return False
    
class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments', verbose_name='Завдання')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField(verbose_name='Текст коментаря')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')
    
    class Meta:
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Коментар від {self.author} до {self.task}'