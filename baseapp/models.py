from django.db import models

# Create your models here.
from django.contrib.auth.models import Group, User

group, created = Group.objects.get_or_create(name='TaskGroup')
group, created = Group.objects.get_or_create(name='NonTaskGroup')

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()