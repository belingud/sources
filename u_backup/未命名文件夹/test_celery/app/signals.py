from django.dispatch import receiver

from django.db.models.signals import post_save, pre_save
from app.models import Test


@receiver(post_save, sender=Test)
def custom_callback(sender, instance, **kwargs):
    print('post save signal')
    print('instance obj: ', instance.name)
    print(kwargs)
    print(sender)
    print('this is a signal test callback method')


@receiver(pre_save, sender=Test)
def pre_save_callback(sender, **kwargs):
    print('pre_save signal')
    print(kwargs)
    print(sender)
    print('finish pre_save callback')


# post_save.connect(custom_callback, sender=Test)
# request_finished.connect(custom_callback)

