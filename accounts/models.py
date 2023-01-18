from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from groups.models import GroupProfile
from posts.models import Post


class Notification(models.Model):
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


class Profile(models.Model):
    User._meta.get_field('email')._nullable = False
    User._meta.get_field('first_name')._nullable = False
    User._meta.get_field('last_name')._nullable = False

    User._meta.get_field('first_name')._blank = False
    User._meta.get_field('last_name')._blank = False

    User._meta.get_field('email')._unique = True

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(null=True, blank=True)
    description = models.TextField()
    avatar = models.ImageField(default='avatar-default.png', blank=True)
    liked_posts = models.ManyToManyField(Post)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Group.objects.create(name="{}{}{}".format(instance.id, instance.username, instance.id))
        group = Group.objects.get(name="{}{}{}".format(instance.id, instance.username, instance.id))
        group.groupprofile.owner = instance
        group.groupprofile.name = "Feed"
        group.groupprofile.is_feed = True
        group.user_set.add(instance)
        group.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(pre_delete, sender=User)
def delete_user_profile(sender, instance, **kwargs):
    group = Group.objects.get(name="{}{}{}".format(instance.id, instance.username, instance.id))
    group.delete()


class FriendRequest(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='From')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='To')
    accepted = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)