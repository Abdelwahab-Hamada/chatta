from channels_graphql_ws import GraphqlWsConsumer

from .schema import schema

import channels

class Consumer(GraphqlWsConsumer):

    async def on_connect(self, payload):
        if not self.scope['user'].is_authenticated:
            #this exception to reject nonlogged clients
            raise Exception("login first")
        print(self.scope["user"] ,'connected to websocket')

    schema=schema

