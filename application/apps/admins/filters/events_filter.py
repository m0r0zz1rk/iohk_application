import datetime

from django.db.models import Q
from django_filters import rest_framework as filters

from apps.admins.models.guides.participant_categories import ParticipantCategories
from apps.commons.utils.data_types.date import DateUtils
from apps.events.models import Events
from apps.events.models.event_types import EventTypes


class EventsFilter(filters.FilterSet):
    """Поля для фильтрации мероприятий"""
    name = filters.CharFilter(
        lookup_expr='icontains'
    )
    description = filters.CharFilter(
        lookup_expr='icontains'
    )
    event_type = filters.CharFilter(
        method='filter_event_type'
    )
    app_date_range = filters.CharFilter(
        method='filter_app_date_range'
    )
    date_range = filters.CharFilter(
        method='filter_date_range'
    )
    categories = filters.CharFilter(
        method='filter_categories'
    )

    def filter_event_type(self, queryset, name, value):
        if not value or value == '':
            return queryset
        type_id = EventTypes.objects.get(name=value).object_id
        queryset = queryset.filter(event_type_id=type_id)
        return queryset

    def filter_app_date_range(self, queryset, name, value):
        if not value or value == '':
            return queryset
        dates = DateUtils.split_date_range(value)
        queryset = queryset.filter(Q(app_date_start__lte=dates[0]) & Q(app_date_end__gte=dates[1]))
        return queryset

    def filter_date_range(self, queryset, name, value):
        if not value or value == '':
            return queryset
        dates = value.split(' - ')
        date_start = datetime.datetime.strptime(
            dates[0],
            '%d.%m.%Y'
        )
        date_end = datetime.datetime.strptime(
            dates[1],
            '%d.%m.%Y'
        )
        queryset = queryset.filter(Q(date_start__lte=date_start) & Q(date_end__gte=date_end))
        return queryset

    def filter_categories(self, queryset, name, value):
        if not value or value == '':
            return queryset
        category_id = ParticipantCategories.objects.get(name=value).object_id
        queryset = queryset.filter(categories__object_id=category_id)
        return queryset

    class Meta:
        model = Events
        exclude = ('date_create', 'object_id')
