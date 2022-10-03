import graphene

from .gql.quieries import Query

from .gql.mutations import Mutation

from chats.gql.subscriptions import Subscription


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
)