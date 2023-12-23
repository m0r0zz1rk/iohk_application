from rest_framework import serializers

from apps.applications.models import AppFieldTypes


class AppFieldTypesSerializer(serializers.ModelSerializer):
    """Сериализация типов полей заявок"""
    class Meta:
        model = AppFieldTypes
        exclude = ('date_create', )
