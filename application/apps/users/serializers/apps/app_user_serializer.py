from rest_framework import serializers


class SelectFieldOptionSerializer(serializers.Serializer):
    """Сериализация возможного значения для поля заявки"""
    option = serializers.CharField(
        max_length=500,
        allow_blank=False,
        label='Возможное значение'
    )


class AppUserSerializer(serializers.Serializer):
    """Сериализация заполненного поля заявки пользователя"""
    object_id = serializers.UUIDField(
        allow_null=False,
        label='ID заполненного поля'
    )
    name = serializers.CharField(
        max_length=250,
        allow_blank=False,
        label='Наименование поля'
    )
    type = serializers.CharField(
        max_length=50,
        allow_blank=False,
        label='Тип поля'
    )
    value = serializers.CharField(
        max_length=5000,
        allow_blank=True,
        label='Значение'
    )
    options = serializers.ListSerializer(
        allow_null=True,
        allow_empty=True,
        child=serializers.CharField(
            max_length=500,
            allow_null=False,
            allow_blank=False,
            label='Возможное значение'
        ),
        label='Список возможных значений'
    )
