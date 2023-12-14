from rest_framework import serializers

from apps.admins.models.guides.event_forms import EventForms
from apps.commons.pagination_serializer import PaginationSerializer


class EventsFormSerializer(serializers.ModelSerializer):
    """Сериализация форм проведения мероприятий"""
    class Meta:
        model = EventForms
        fields = ('object_id', 'name')


class EventsFormPaginationSerializer(PaginationSerializer):
    """Сериализация данных при пагинации форм проведения мероприятий"""
    results = EventsFormSerializer(many=True)


class EventsFormSaveSerializer(serializers.ModelSerializer):
    """Сериализация данных при добавлении новой формы проведения мероприятия"""
    class Meta:
        model = EventForms
        fields = ('name',)
