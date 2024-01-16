from rest_framework import serializers

from apps.applications.models import Apps
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
    entity_id = serializers.UUIDField(
        allow_null=False,
        label='Object_id сущности'
    )
    message = serializers.CharField(
        max_length=2000,
        allow_blank=True,
        allow_null=True,
        label='Сообщение по заявке'
    )
    status = serializers.CharField(
        max_length=30,
        allow_null=False,
        allow_blank=False,
        label='Новый статус'
    )
    result = serializers.CharField(
        max_length=10000,
        label='Результат заявки (HTML код из TinyMCE)'
    )


class AppsListSerializer(serializers.ModelSerializer):
    """Сериализация данных при получении списка заявок"""
    event_type = serializers.SerializerMethodField(
        label='Тип мероприятия'
    )
    event_name = serializers.SerializerMethodField(
        label='Наименование мероприятия'
    )
    event_date_range = serializers.SerializerMethodField(
        label='Сроки проведения мероприятия'
    )
    app_status = serializers.SerializerMethodField(
        label='Статус заявки'
    )

    def get_event_type(self, obj):
        return obj.event.event_type.name

    def get_event_name(self, obj):
        return obj.event.name

    def get_event_date_range(self, obj):
        return f'{obj.event.date_start.strftime('%d.%m.%Y')}-{obj.event.date_end.strftime('%d.%m.%Y')}'

    def get_app_status(self, obj):
        return obj.get_status_display()

    class Meta:
        model = Apps
        fields = (
            'object_id',
            'date_create',
            'date_update',
            'event_id',
            'event_type',
            'event_name',
            'event_date_range',
            'app_status'
        )
