import datetime
from datetime import timedelta

from django.db.models import Q
from django_filters import rest_framework as filters

from apps.commons.consts.journals.journal_event_results import JOURNAL_EVENT_RESULTS
from apps.commons.consts.journals.journal_rec_types import JOURNAL_REC_TYPES
from apps.journals.models import Journal


class JournalFilter(filters.FilterSet):
    """Поля для фильтрации записей журнала"""
    event_time = filters.CharFilter(
        method='filter_event_time'
    )
    source = filters.CharFilter(
        lookup_expr='icontains'
    )
    rec_type = filters.CharFilter(method='filter_type')
    event_result = filters.CharFilter(method='filter_result')
    description = filters.CharFilter(
        lookup_expr='icontains'
    )

    def filter_event_time(self, queryset, name, value):
        get_day = datetime.datetime.strptime(value, '%d.%m.%Y')
        tomorrow = get_day + datetime.timedelta(days=1)
        queryset = queryset.filter(Q(event_time__gte=get_day)&Q(event_time__lt=tomorrow))
        return queryset

    def filter_result(self, queryset, name, value):
        filter_value = ''
        for source, display in JOURNAL_EVENT_RESULTS:
            if display == value:
                filter_value = source
                break
        queryset = queryset.filter(event_result=filter_value)
        return queryset

    def filter_type(self, queryset, name, value):
        filter_value = ''
        for source, display in JOURNAL_REC_TYPES:
            if display == value:
                filter_value = source
                break
        queryset = queryset.filter(rec_type=filter_value)
        return queryset

    class Meta:
        model = Journal
        fields = '__all__'
