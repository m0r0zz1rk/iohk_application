from django.core.validators import MinValueValidator
from rest_framework import serializers

from apps.admins.models.guides.event_types import EventTypes


class EventsTypeSerializer(serializers.ModelSerializer):
    """Сериализация типа мероприятий"""
    class Meta:
        model = EventTypes
        fields = ('object_id', 'name')


class EventsTypesSaveSerializer(serializers.ModelSerializer):
    """Сериализация данных при добавлении нового типа мероприятия"""
    class Meta:
        model = EventTypes
        fields = ('name',)


class EventsTypesCountSerializer(serializers.Serializer):
    """Сериализация количества типов мероприятий в АИС"""
    count = serializers.IntegerField(
        validators=[MinValueValidator(0),]
    )
