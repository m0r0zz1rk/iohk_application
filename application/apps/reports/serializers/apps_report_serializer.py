from rest_framework import serializers


class AppsReportSerializer(serializers.Serializer):
    """Сериализация данных для генерации Excel отчета с заявками на мероприятие"""
    event_id = serializers.UUIDField(
        allow_null=False,
        label='Object_id мероприятия'
    )
    apps_types = serializers.CharField(
        min_length=3,
        max_length=4,
        allow_null=False,
        allow_blank=False,
        label='Типы заявок'
    )
