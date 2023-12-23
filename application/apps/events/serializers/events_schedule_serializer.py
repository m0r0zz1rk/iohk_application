from rest_framework import serializers

from apps.commons.serializers.pagination_serializer import PaginationSerializer
from apps.events.models import EventsSchedule, EventForms
from apps.events.utils.events_schedule import EventsScheduleUtils


class EventsScheduleSerializer(serializers.ModelSerializer):
    """Сериализация данных о расписании мероприятия"""
    form = serializers.SlugRelatedField(
        slug_field='name',
        queryset=EventForms.objects.all(),
        label='Форма проведения'
    )
    warning = serializers.SerializerMethodField(
        label='Проверка на пересечения'
    )

    def get_warning(self, obj):
        return EventsScheduleUtils.check_part_cross_to_another(obj.object_id)

    class Meta:
        model = EventsSchedule
        fields = ['object_id', 'start', 'end', 'theme', 'form', 'url', 'address', 'warning']


class EventsSchedulePaginationSerializer(PaginationSerializer):
    """Сериализация пагинационных данных о расписании мероприятия"""
    results = EventsScheduleSerializer(many=True)


class EventScheduleSaveSerializer(serializers.ModelSerializer):
    """Сериализация модели мероприятий"""
    form = serializers.SlugRelatedField(
        slug_field='name',
        queryset=EventForms.objects.all(),
        label='Форма проведения'
    )

    class Meta:
        model = EventsSchedule
        exclude = ('object_id', 'date_create', 'event')


class EventScheduleModelSerializer(serializers.ModelSerializer):
    """Сериализация модели мероприятий"""
    form = serializers.SlugRelatedField(
        slug_field='name',
        queryset=EventForms.objects.all(),
        label='Форма проведения'
    )

    class Meta:
        model = EventsSchedule
        exclude = ('object_id', 'date_create')
