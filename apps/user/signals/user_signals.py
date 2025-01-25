from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.user.helpers.user_helper_functions import send_otp_via_thread, set_user_otp
from apps.user.models.user_models import UserProfile


@receiver(pre_save, sender=UserProfile)
def pre_save_user_profile(sender, instance, **kwargs):
    if not instance.pk:
        instance = set_user_otp(instance)


@receiver(post_save, sender=UserProfile)
def post_save_user_profile(sender, instance, created, **kwargs):
    if created:
        send_otp_via_thread(instance)
