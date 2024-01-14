from rest_framework import serializers


class AppsCountSerializer(serializers.Serializer):
    """Сериализация данных при получении количества заявок по мероприятию"""
    event_name = serializers.CharField(
        max_length=500,
        allow_null=False,
        allow_blank=False,
        label='Наименование мероприятия'
    )
    event_date_range = serializers.CharField(
        max_length=21,
        allow_blank=False,
        allow_null=False,
        label='Срок проведения мероприятия'
    )
    apps_count = serializers.IntegerField(
        min_value=0,
        label='Количество заявок'
    )
