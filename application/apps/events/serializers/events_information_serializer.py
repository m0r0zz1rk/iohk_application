from rest_framework import serializers
from tinymce import models

from apps.events.models import EventsInformation


class EventsInformationSerializer(serializers.ModelSerializer):
    """Сериализация информационных сообщений о мероприятиях"""
    class Meta:
        model = EventsInformation
        fields = ['info', ]


class EventsInformationSaveSerializer(serializers.Serializer):
    """Сериализация данных при сохранении информационного сообщения"""
    info = serializers.CharField(
        max_length=10000,
        label='HTML код из TinyMCE'
    )
