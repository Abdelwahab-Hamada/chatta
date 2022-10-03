import graphene
from graphene_django import DjangoObjectType

from .models import Chat,Message

import textwrap

class MessageType(DjangoObjectType):
    class Meta:
        model=Message
        fields='__all__'
    read_time_ago=graphene.String()
    sender=graphene.String()

    def resolve_read_time_ago(self,info):#self is message instance
        current_user=info.context.user
        sender=self.sender
        
        if current_user == sender :
            return f'read {self.get_read_time()}' if self.is_read else f'sent {self.get_sent_time()}'
        return f'recieved {self.get_sent_time()}'

    def resolve_sender(self,info):
        current_user=info.context.user
        sender=self.sender

        if current_user == sender:
            return 'you'
        return sender.username

class ChatType(DjangoObjectType):
    class Meta:
        model=Chat
        fields='__all__'
    unread_messages=graphene.List(MessageType)
    last_message=graphene.Field(MessageType)
    recipient_status=graphene.String()

    def resolve_unread_messages(self,_):
        return self.get_unread_messages()

    def resolve_last_message(self,_):
        return self.get_last_message()

    def resolve_recipient_status(self,info):
        current_user=info.context.user
        recipient=self.recipients.exclude(pk=current_user.id)[0]#other user
        
        return recipient.logs.status()
