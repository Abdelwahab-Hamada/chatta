import graphene
from graphene_django import DjangoObjectType

from django.contrib.auth.models import User

from chats.types import ChatType

from chats.models import Chat

class UserType(DjangoObjectType):
    class Meta:
        model=User
        fields=('username','id')
    status=graphene.String() 
    chat=graphene.Field(ChatType)
    
    def resolve_username(self,_):
        return f'@{self.username}'

    def resolve_status(self,_):
        logs=self.logs
        return logs.get_status()

    def resolve_chat(self,info):
        current_user=info.context.user
        chat,created=Chat.objects.filter(recipients=current_user).get_or_create(recipients__pk=self.id)

        # chat.subscribers.add(current_user)

        if created:
            current_user.logs.friends.add(self)
            self.logs.friends.add(current_user)
            chat.recipients.add(current_user)
            chat.recipients.add(self)

        return chat

    
    
