from rest_framework import serializers

from apps.applications.serializers.app_form_fields_serializer import AppFormFieldSaveSerializer


class AppSaveSerializer(serializers.Serializer):
    """Сериализация данных при сохранении заявки"""
    event_id = serializers.UUIDField(
        allow_null=False,
        label='Object ID мероприятия'
    )
    fields = AppFormFieldSaveSerializer(many=True)


class AppChangeStatusSerializer(serializers.Serializer):
    """Сериализация данных при изменении статуса заявки"""
    event_id = serializers.UUIDField(
        allow_null=False,
        label='Object_id мероприятия'
    )
    status = serializers.CharField(
        max_length=30,
        allow_null=False,
        allow_blank=False,
        label='Новый статус'
    )
