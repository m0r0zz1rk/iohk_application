from rest_framework import serializers

from apps.admins.models.guides.event_types import EventTypes
from apps.commons.pagination_serializer import PaginationSerializer


class EventsTypeSerializer(serializers.ModelSerializer):
    """Сериализация типа мероприятий"""
    class Meta:
        model = EventTypes
        fields = ('object_id', 'name')


class EventsTypePaginationSerializer(PaginationSerializer):
    """Сериализация данных при пагинации типов мероприятий"""
    results = EventsTypeSerializer(many=True)


class EventsTypesSaveSerializer(serializers.ModelSerializer):
    """Сериализация данных при добавлении нового типа мероприятия"""
    class Meta:
        model = EventTypes
        fields = ('name',)
