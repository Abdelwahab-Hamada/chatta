from django.db import models
from django.conf import settings
from django.db.models.signals import (
    post_save,
    pre_save
)
from django.dispatch import receiver

from django.utils import timezone
import humanize


class Log(models.Model):
    user=models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='logs'
    )
    online=models.BooleanField(default=False)
    last_seen=models.DateTimeField(auto_now_add=True)
    friends= models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='friend_logs')


    def __str__(self):
        return str(self.user)

    def get_status(self):
        if self.online:
            return 'online'
        now= timezone.now()
        last_seen=self.last_seen
        return f"last seen {humanize.naturaltime(now - last_seen)}"

    def set_last_seen(self):
        self.online=False

        print(self.user,'is offline')

        now= timezone.now()
        self.last_seen=now
        self.save()

        self.user.subscribed_chats.remove(*self.user.subscribed_chats.all())

    def set_online(self):
        self.online=True

        print(self.user,'is online')

        self.save()

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def user_created_handler(sender,instance,created,*args,**kwargs):
    if created:
        Log.objects.create(user=instance)
        print('user`s logs created')