import datetime

from django.db.models import Q
from django_filters import rest_framework as filters

from apps.admins.models.guides.participant_categories import ParticipantCategories
from apps.commons.utils.data_types.date import DateUtils
from apps.events.models import Events, EventsInformation
from apps.events.models.event_types import EventTypes


class EventsInformationFilter(filters.FilterSet):
    """Поля для фильтрации информационных сообщений о мероприятии"""
    event = filters.CharFilter(
        method='filter_event'
    )

    def filter_event(self, queryset, name, value):
        if not value or value == '':
            return queryset
        event_id = Events.objects.get(name=value).object_id
        queryset = queryset.filter(event_id=event_id)
        return queryset

    class Meta:
        model = EventsInformation
        fields = ('event', )
