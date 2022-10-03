import graphene
from graphene_django import DjangoObjectType

class LogType(DjangoObjectType):
    class Meta:
        model=Log
        fields='__all__'