from rest_framework import serializers


class CountReportEventSerializer(serializers.Serializer):
    """Сериализация данных о мероприятии для количественного отчета"""
    id = serializers.IntegerField(
        min_value=1,
        label='ID мероприятия'
    )
    event_id = serializers.UUIDField(
        allow_null=False,
        label='Object_id мероприятия'
    )


class CountReportFilterSerializer(serializers.Serializer):
    """Сериализация данных о фильтре для количественного отчета"""
    id = serializers.IntegerField(
        min_value=1,
        label='ID фильтра'
    )
    field = serializers.CharField(
        max_length=250,
        allow_null=False,
        allow_blank=False,
        label='Наименование поля'
    )
    value = serializers.CharField(
        max_length=5000,
        allow_blank=False,
        allow_null=False,
        label='Значение'
    )


class CountReportSerializer(serializers.Serializer):
    """Сериализация данных о количественном отчете"""
    apps_types = serializers.CharField(
        min_length=3,
        max_length=4,
        allow_null=False,
        allow_blank=False,
        label='Тип заявок'
    )
    events = CountReportEventSerializer(
        many=True,
        label='Мероприятия'
    )
    filters = CountReportFilterSerializer(
        many=True,
        label='Фильтры'
    )
    total_row = serializers.BooleanField(
        label='Итоговая строка'
    )

