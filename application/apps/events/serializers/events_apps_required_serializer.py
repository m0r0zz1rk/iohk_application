from rest_framework import serializers

from apps.events.models import EventsAppsRequired


class EventsAppsRequiredSerializer(serializers.ModelSerializer):
    """Сериализация записей о необходимости форм заявок для мероприятий"""
    class Meta:
        model = EventsAppsRequired
        fields = ('event_id', 'user_app_required', 'participant_app_required')


class EventsAppsRequiredChangeSerializer(serializers.Serializer):
    """Сериализация данных при поступлении запроса на изменение необходимости формы заявки"""
    event_id = serializers.UUIDField(
        allow_null=False,
        label='Ojbect_id мероприятия'
    )
    type = serializers.CharField(
        max_length=25,
        allow_null=False,
        allow_blank=False,
        label='Тип заявки'
    )
    value = serializers.BooleanField(
        label='Использование'
    )
