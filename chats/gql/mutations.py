import graphene
import graphql_jwt
from graphql_jwt.decorators import login_required

from chats.models import Chat,Message

from chats.types import MessageType,ChatType

from django.contrib.auth.models import User

from .subscriptions import ChatSubscription

class ChatJointement(graphene.Mutation):
    class Arguments:
        recipient_id=graphene.String()
    is_joined=graphene.Boolean()

    def mutate(_,info,recipient_id):
        current_user=info.context.user
        recipient=User.objects.get(pk=recipient_id)

        chat,is_created=Chat.objects.filter(recipients=current_user).get_or_create(recipients__pk=recipient_id)
        
        if is_created:
            current_user.logs.friends.add(recipient)
            recipient.logs.friends.add(current_user)
            chat.recipients.add(current_user)
            chat.recipients.add(recipient)
        else:
            for message in chat.get_unread_messages().filter(sender__pk=recipient_id):
                message.set_read_time()

        chat.subscribers.add(current_user)

        return ChatJointement(is_joined=True)

class ChatLeaving(graphene.Mutation):
    is_leaved=graphene.Boolean()

    def mutate(_,info):
        current_user=info.context.user

        subscribed_chats=current_user.subscribed_chats
        subscribed_chats.remove(*subscribed_chats.all())

        print(current_user,'left chat')

        # chat=Chat.objects.get(pk=chat_id)

        # chat.subscribers.remove(current_user)

        # print(current_user,'unsubscribed',chat_id)

        return ChatLeaving(is_leaved=True)

class SendingMessage(graphene.Mutation):
    class Arguments:
        recipient_id = graphene.String()
        text = graphene.String()
    message=graphene.Field(MessageType)

    def mutate(_,info,recipient_id,text):
        current_user=info.context.user

        chat=Chat.objects.filter(recipients=current_user).get(recipients__pk=recipient_id)

        recipient=User.objects.get(pk=recipient_id)

        message=chat.messages.create(
            text=text,
            sender=current_user,
        )

        if recipient in chat.subscribers.all():
            message.set_read_time()

        ChatSubscription.send_new_message(message=message)

        return SendingMessage(message=message) 



