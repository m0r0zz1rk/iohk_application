from rest_framework import serializers

from apps.applications.models import Apps


class AdminAppsListSerializer(serializers.ModelSerializer):
    """Сериализация данных при получении списка заявок в ЛК администратора"""
    fio = serializers.SerializerMethodField(
        label='ФИО пользователя'
    )
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

    def get_fio(self, obj):
        try:
            return obj.profile.get_display_name()
        except Exception:
            return '(Удаленный пользователь)'

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
            'fio',
            'event_type',
            'event_name',
            'event_date_range',
            'app_status'
        )