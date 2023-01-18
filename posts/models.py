from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group


class Post(models.Model):
    slug = models.SlugField()
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    host_group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    media = models.FileField(blank=True)
    type = models.IntegerField(default=0, blank=False)
    likes = models.IntegerField(default=0, blank=False)


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)


class Message(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE)
    text = models.TextField()
