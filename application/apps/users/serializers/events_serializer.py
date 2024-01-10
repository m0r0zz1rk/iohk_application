from rest_framework import serializers

from apps.events.models import Events


class EventsShortInfoSerializer(serializers.ModelSerializer):
    """Сериализация краткой информации по мероприятиям"""
    app_date_range = serializers.SerializerMethodField(label='Сроки подачи заявок')
    date_range = serializers.SerializerMethodField(label='Сроки проведения')
    categories = serializers.SerializerMethodField(label='Категории участников')

    def get_app_date_range(self, obj):
        return (f'{obj.app_date_start.strftime('%d.%m.%Y')} - '
                f'{obj.app_date_end.strftime('%d.%m.%Y')}')

    def get_date_range(self, obj):
        return (f'{obj.date_start.strftime('%d.%m.%Y')} - '
                f'{obj.date_end.strftime('%d.%m.%Y')}')

    def get_categories(self, obj):
        cats = []
        for cat in obj.categories.all():
            cats.append(cat.name)
        return cats

    class Meta:
        model = Events
        fields = (
            'object_id',
            'name',
            'description',
            'app_date_range',
            'date_range',
            'categories'
        )


class EventAppsRequiredSerializer(serializers.Serializer):
    """Сериализация необходимости форм заявок на мероприятие"""
    user_app = serializers.BooleanField(
        default=False,
        label='Заявка пользователя'
    )
    part_app = serializers.BooleanField(
        default=False,
        label='Заявки участников от пользователя'
    )