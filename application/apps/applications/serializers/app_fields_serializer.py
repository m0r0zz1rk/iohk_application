from typing import Optional

from rest_framework import serializers

from apps.applications.models import AppFields, AppFieldTypes
from apps.applications.utils.field_available_values import FieldAvailableValuesUtils


class AppFieldsSerializer(serializers.ModelSerializer):
    """Сериализация полей формы заявки на мероприятие"""
    type = serializers.SlugRelatedField(
        slug_field='type',
        queryset=AppFieldTypes.objects.all()
    )
    available_values = serializers.SerializerMethodField()

    def get_available_values(self, obj) -> Optional[list]:
        if obj.type.type in ['Выбор из списка', 'Множественный выбор из списка']:
            values = []
            available = FieldAvailableValuesUtils.get_available_values_for_field(obj.object_id)
            if available is not None:
                for value in available:
                    values.append(value.option)
            return values
        return None

    class Meta:
        model = AppFields
        fields = ('object_id', 'event_id', 'user_app', 'name', 'type', 'available_values')


class ShortAppFieldSerializer(serializers.ModelSerializer):
    """Сериализация краткой информации о поле формы заявки"""
    type = serializers.SlugRelatedField(
        slug_field='alias',
        queryset=AppFieldTypes.objects.all()
    )
    available_values = serializers.SerializerMethodField()

    def get_available_values(self, obj) -> Optional[list]:
        if obj.type.type in ['Выбор из списка', 'Множественный выбор из списка']:
            values = []
            available = FieldAvailableValuesUtils.get_available_values_for_field(obj.object_id)
            if available is not None:
                for value in available:
                    values.append(value.option)
            return values
        return None

    class Meta:
        model = AppFields
        fields = ('object_id', 'name', 'type', 'available_values')


class ManyAppFieldsSerializer(serializers.Serializer):
    """Сериализация списка полей формы заявки на мероприятие"""
    fields = AppFieldsSerializer(many=True, label='Поля')


class AppFieldSaveSerializer(serializers.ModelSerializer):
    """Сериализация данных при добавлении нового поля формы заявки"""
    type = serializers.SlugRelatedField(
        slug_field='type',
        queryset=AppFieldTypes.objects.all()
    )

    class Meta:
        model = AppFields
        fields = ('event', 'user_app', 'name', 'type')
