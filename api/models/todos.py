from django.db import models
from .accounts import User

class Todo(models.Model):
    user = models.ForeignKey(User, related_name='todos', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)