import graphene
from channels_graphql_ws import Subscription

from graphql_jwt.decorators import login_required

from chats.types import MessageType

class ChatSubscription(Subscription):
    message=graphene.Field(MessageType)

    class Arguments:
        chat_id = graphene.String()
        
    @login_required
    def subscribe(self, info, chat_id=None):
        user=info.context.user
        username=user.username
        
        subscription='notifications' if chat_id is None else chat_id
        print(username,'subscribed to',subscription)

        return [chat_id] if chat_id is not None else [username]
    

    @login_required
    def publish(payload, info,chat_id=None):
        message=payload["message"]

        return ChatSubscription(
            message=message
        )

    @classmethod
    def send_new_message(cls, message):
        chat=message.chat

        cls.broadcast(
            group=str(chat.id),
            payload={'message':message},
        )

        for recipient in chat.recipients.all():
            recipient_username=recipient.username
            cls.broadcast(
                group=recipient_username,
                payload={'message':message},
            )

    # @classmethod
    # def unsubscribe_chat(cls, chat_id):#stops all subscriptions
    #     print('all subs are unconnected',chat_id)
    #     cls.unsubscribe(
    #         group=chat_id,
    #     )

class Subscription(graphene.ObjectType):
    subscribe_chat = ChatSubscription.Field()

    