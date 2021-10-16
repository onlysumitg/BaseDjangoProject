from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.
class Todo(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="todo", on_delete=models.CASCADE)
    task = models.CharField(max_length=160)
    created = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(auto_now=True)

    completed = models.BooleanField(default=False)

    @classmethod
    def add(cls, user, task,):

        todo = cls.objects.create(user=user, task=task)
        return todo

    class Meta:
        ordering = ("-completed_on",)
