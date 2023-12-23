from rest_framework import serializers

from apps.applications.models import FieldAvailableValues


class FieldAvailableValuesSerializer(serializers.ModelSerializer):
    """Сериализация возможных значений полей заявки"""
    class Meta:
        model = FieldAvailableValues
        exclude = ('date_create', )


class FieldAvailableValueGiveSerializer(serializers.ModelSerializer):
    """Сериализация полученных данных при сохранении возможного значения поля заявки"""
    class Meta:
        model = FieldAvailableValues
        fields = ('option', )


class FieldAvailableValueSaveSerializer(serializers.ModelSerializer):
    """Сериализация полученных данных при сохранении возможного значения поля заявки"""
    class Meta:
        model = FieldAvailableValues
        fields = ('option', 'field')
