from rest_framework import serializers

from apps.commons.serializers.pagination_serializer import PaginationSerializer
from apps.events.models import EventTypes
from apps.events.models.events import Events


class EventsSerializer(serializers.ModelSerializer):
    """Сериализация данных о мероприятий"""
    event_type = serializers.SlugRelatedField(
        slug_field='name',
        queryset=EventTypes.objects.all()
    )
    app_date_range = serializers.SerializerMethodField()
    date_range = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

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
            'event_type',
            'event_status',
            'app_date_range',
            'date_range',
            'categories'
        )


class EventsPaginationSerializer(PaginationSerializer):
    """Сериализация пагинационных данных мероприятий"""
    results = EventsSerializer(many=True)


class EventGetSerializer(serializers.Serializer):
    """Сериализация запроса для получения мероприятия"""
    event_id = serializers.UUIDField(
        allow_null=False,
        label='Object_id мероприятия'
    )


class EventSaveSerializer(EventsSerializer):
    """Сериализация данных при сохранении мероприятия"""
    event_type = serializers.CharField(
        max_length=100,
        allow_null=False,
        allow_blank=False,
        label='Тип мероприятия'
    )
    app_date_range = serializers.CharField(
        max_length=25,
        allow_null=False,
        allow_blank=False,
        label='Сроки подачи заявки (в формате: дд.мм.гггг - дд.мм.гггг)'
    )
    date_range = serializers.CharField(
        max_length=25,
        allow_null=False,
        allow_blank=False,
        label='Сроки проведения мероприятия (в формате: дд.мм.гггг - дд.мм.гггг)'
    )
    categories = serializers.ListField(
        allow_null=False,
        allow_empty=False,
        label='Категории участников'
    )


class EventModelSerializer(serializers.ModelSerializer):
    """Сериализация модели мероприятий"""
    class Meta:
        model = Events
        exclude = ('object_id', 'date_create')


class EventsShortSerializer(serializers.ModelSerializer):
    """Сериализация данных при получении списка с краткой информацией о мероприятиях"""
    date_range = serializers.SerializerMethodField(
        label='Сроки проведения мероприятия'
    )

    def get_date_range(self, obj):
        return (f'{obj.date_start.strftime('%d.%m.%Y')}-'
                f'{obj.date_end.strftime('%d.%m.%Y')}')

    class Meta:
        model = Events
        fields = ('object_id', 'name', 'date_range', 'event_status')
