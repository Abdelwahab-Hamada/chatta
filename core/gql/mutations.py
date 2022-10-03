import graphene
import graphql_jwt
from graphql_jwt.decorators import login_required

from chats.gql.mutations import (
    ChatJointement,
    SendingMessage,
    ChatLeaving,
)

from core.types import UserType

from django.contrib.auth.models import User

from logs.models import Log

from django.contrib.auth import login,logout


class Offline(graphene.Mutation):
    is_offline=graphene.Boolean()

    def mutate(_,info):
        current_user=info.context.user
        subscribed_chats=current_user.subscribed_chats
        subscribed_chats.remove(*subscribed_chats.all())

        current_user.logs.set_last_seen()

        return Offline(is_offline=True)

class Online(graphene.Mutation):
    is_online=graphene.Boolean()

    def mutate(_,info):
        current_user=info.context.user

        login(info.context,current_user,backend='graphql_jwt.backends.JSONWebTokenBackend')
        
        current_user.logs.set_online()

        return Online(is_online=True)

class Register(graphene.Mutation):
    class Arguments:
        username=graphene.String(required=True)
        password=graphene.String(required=True)
    is_registered=graphene.Boolean()

    @classmethod
    def mutate(cls,root,info,username,password):
        user=User.objects.create_user(
            username=username,
            password=password)

        Log.objects.create(user=user)

        return Register(is_registered=True)

class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        current_user=info.context.user
        current_user.logs.set_online()
            
        login(info.context,current_user)
        return cls(user=current_user)

class Logout(graphene.Mutation):
    is_loggedout = graphene.Boolean()

    @login_required
    def mutate(self, info):
        current_user=info.context.user

        subscribed_chats=current_user.subscribed_chats
        subscribed_chats.remove(*subscribed_chats.all())

        logout(info.context)

        current_user.logs.set_last_seen()
        
        print(current_user,'loggedout')

        return Logout(is_loggedout=True)

class Mutation(graphene.ObjectType):
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    delete_token_cookie = graphql_jwt.DeleteJSONWebTokenCookie.Field()
    delete_refresh_token_cookie = graphql_jwt.DeleteRefreshTokenCookie.Field()

    join_chat=ChatJointement.Field()
    leave_chat=ChatLeaving.Field()
    send_message=SendingMessage.Field()

    online_me=Online.Field()
    offline_me=Offline.Field()

    register_me=Register.Field()
    logout_me=Logout.Field() 