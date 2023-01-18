from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver


def is_member(user, group):
    return user.groups.filter(name=group.name).exists()


def is_admin(user, group):
    return group.user_set.filter(id=user.id).exists()


class GroupProfile(models.Model):
    name = models.TextField(default="Feed")
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    avatar = models.ImageField(default='avatar-default.png', blank=True)
    is_feed = models.BooleanField(default=False)
    description = models.TextField()


@receiver(post_save, sender=Group)
def create_group_profile(sender, instance, created, **kwargs):
    if created:
        GroupProfile.objects.create(group=instance)
        instance.groupprofile.name = instance.name
        instance.save()


@receiver(post_save, sender=Group)
def save_group_profile(sender, instance, **kwargs):
    instance.groupprofile.save()
