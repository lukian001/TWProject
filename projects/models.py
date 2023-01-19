from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Instance(models.Model):
    name = models.CharField(max_length=30)
    code = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
