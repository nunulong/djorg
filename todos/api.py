from django.conf import settings
from rest_framework import serializers, viewsets
from .models import Todo

# Serializer define the API representation


class TodoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'content')

    def create(self, validated_data):
        user = self._context['request'].user
        todo = Todo.objects.create(user=user, **validated_data)
        return todo


# viewsets define the view behavior
class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.none()

    def get_queryset(self):
        user = self.request.user
        if settings.DEBUG:
            return Todo.objects.all()
        if user.is_anonymous:
            return Todo.objects.none()
        else:
            return Todo.objects.filter(user=user)
