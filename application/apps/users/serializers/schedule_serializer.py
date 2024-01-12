from rest_framework import serializers

from apps.events.models import EventsSchedule, EventForms


class ScheduleSerializer(serializers.ModelSerializer):
    """Сериализация данных при получении расписания занятий в ЛК пользователя"""
    form = serializers.SlugRelatedField(
        slug_field='name',
        queryset=EventForms.objects.all()
    )

    class Meta:
        model = EventsSchedule
        fields = ('start', 'end', 'theme', 'form', 'url', 'address')