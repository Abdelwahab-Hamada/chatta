from django.db import models
from django.utils import timezone
from django.conf import settings

import uuid
import textwrap

import humanize


class Chat(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipients= models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='chats')
    subscribers= models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='subscribed_chats')

    def __str__(self):
        return str([str(member) for member in self.recipients.all()])

    def get_unread_messages(self):
        return self.messages.filter(is_read=False)

    def get_last_message(self):
        return self.messages.order_by('sent_on').last()

class Message(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text= models.TextField()
    chat= models.ForeignKey(Chat,related_name='messages',on_delete=models.CASCADE)
    sender= models.ForeignKey(settings.AUTH_USER_MODEL,related_name='messages',on_delete=models.CASCADE)
    sent_on=models.DateTimeField(auto_now_add=True)
    is_read=models.BooleanField(default=False)
    read_on=models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return textwrap.shorten(self.text, width=10, placeholder="...")

    def get_sent_time(self):
        now= timezone.now()
        time_sent= self.sent_on
        readable_time=humanize.naturaltime(now - time_sent)
        return readable_time
    
    def get_read_time(self):
        now= timezone.now()
        time_read= self.read_on
        readable_time=humanize.naturaltime(now - time_read)
        return readable_time

    def set_read_time(self):
        now= timezone.now()
        self.is_read=True
        self.read_on=now
        self.save()