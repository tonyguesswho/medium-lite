from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User
from ipublish.apps.profiles.models import Profile


@receiver(post_save, sender=User)
def create_related_profile(sender, instance, created, *args, **kwargs):

    if instance and created:
        instance.profile = Profile.objects.create(user=instance)

