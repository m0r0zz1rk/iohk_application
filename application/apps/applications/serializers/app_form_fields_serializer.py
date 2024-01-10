from rest_framework import serializers


class AppFormFieldSerializer(serializers.Serializer):
    """Сериализация данных значения поля заявки"""
    field_id = serializers.UUIDField(
        allow_null=False,
        label='Object_id поля заявки'
    )
    form_field_id = serializers.UUIDField(
        allow_null=False,
        label='Object_id заполненного поля заявки'
    )
    value = serializers.CharField(
        max_length=5000,
        allow_blank=True,
        label='Значение'
    )


class AppFormFieldSaveSerializer(serializers.Serializer):
    """Сериализация данных при сохранении значения поля заявки"""
    field_id = serializers.UUIDField(
        allow_null=False,
        label='Object_id поля заявки'
    )
    value = serializers.CharField(
        max_length=5000,
        allow_blank=True,
        label='Значение'
    )


class PartAppFormRecSerializer(serializers.Serializer):
    """Сериализация записей заполненных полей заявок участников от пользователя"""
    rec_id = serializers.IntegerField(
        min_value=1,
        label='Номер строки'
    )
    fields = AppFormFieldSerializer(
        many=True,
        label='Заполненные поля'
    )


class PartAppFormRecSaveSerializer(serializers.Serializer):
    """Сериализация данных при сохранении заявки участника от пользователя"""
    rec_id = serializers.IntegerField(
        min_value=1,
        label='Номер строки'
    )
    fields = AppFormFieldSaveSerializer(
        many=True,
        label='Заполненные поля'
    )


class PartAppFormRecDeleteSerializer(serializers.Serializer):
    """Сериализация данных для удаления заявки участника от пользователя"""
    event_id = serializers.UUIDField(
        allow_null=False,
        label='Object_id мероприятия'
    )
    rec_id = serializers.IntegerField(
        min_value=1,
        label='Номер записи'
    )

