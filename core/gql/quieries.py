import graphene

from core.types import UserType

from django.db.models import Max

from django.contrib.auth.models import User

from chats.types import ChatType

from chats.models import Chat


class Query(graphene.ObjectType):
    friends=graphene.List(UserType)
    others=graphene.List(UserType)
    chat=graphene.Field(ChatType,recipient_id=graphene.String())

    def resolve_friends(_,info):
        current_user=info.context.user
        friends=current_user.logs.friends.all().annotate(last_message=Max('chats__messages__sent_on')).order_by('-last_message')
        
        return friends

    def resolve_others(_,info):
        current_user=info.context.user
        friends=current_user.logs.friends.all()
        others=User.objects.exclude(pk__in=friends).exclude(pk=current_user.id)

        return others

    def resolve_chat(_,info,recipient_id):#for uptodated chat friends
        current_user=info.context.user
        recipient=User.objects.get(pk=recipient_id)

        chat,created=Chat.objects.filter(recipients=current_user).get_or_create(recipients__pk=recipient.id)

        if created:
            current_user.logs.friends.add(recipient)
            recipient.logs.friends.add(current_user)
            chat.recipients.add(current_user)
            chat.recipients.add(recipient)

        return chat
