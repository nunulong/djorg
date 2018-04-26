from graphene_django import DjangoObjectType
import graphene
from .models import Todo as TodoModel


class Todo(DjangoObjectType):
    """"transform data to graphene representation"""
    class Meta:
        model = TodoModel
        interfaces = (graphene.relay.Node, )


class Query(graphene.ObjectType):
    """expose data results."""
    todos = graphene.List(Todo)

    def resolve_todos(self, info):
        user = info.context.user
        if user.is_anonymous:
            return TodoModel.objects.none()
        else:
            return TodoModel.objects.filter(user=user)


schema = graphene.Schema(query=Query)
