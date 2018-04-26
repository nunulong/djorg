from graphene_django import DjangoObjectType
import graphene
from notes.models import Note as NoteModel
from todos.models import Todo as TodoModel


class Note(DjangoObjectType):
    """"transform data to graphene representation"""
    class Meta:
        model = NoteModel
        interfaces = (graphene.relay.Node, )


class Todo(DjangoObjectType):
    class Meta:
        model = TodoModel
        interfaces = (graphene.relay.Node, )


class Query(graphene.ObjectType):
    """expose data results."""
    notes = graphene.List(Note)
    todos = graphene.List(Todo)

    def resolve_notes(self, info):
        user = info.context.user
        if user.is_anonymous:
            return NoteModel.objects.none()
        else:
            return NoteModel.objects.filter(user=user)

    def resolve_todos(self, info):
        user = info.context.user
        if user.is_anonymous:
            return TodoModel.objects.none()
        else:
            return TodoModel.objects.filter(user=user)


schema = graphene.Schema(query=Query)
