import datetime

from django.db.models import Q
from django_filters import rest_framework as filters

from apps.applications.models import Apps
from apps.commons.consts.apps.app_statuses import APP_STATUSES
from apps.events.models import Events


class AppsFilter(filters.FilterSet):
    """Поля для фильтрации заявок пользователя"""
    date_create = filters.CharFilter(
        method='filter_date_create'
    )
    date_update = filters.DateFilter(
        field_name='date_update'
    )
    event_type = filters.CharFilter(
        method='filter_event_type'
    )
    event_name = filters.CharFilter(
        method='filter_event_name'
    )
    event_date_range = filters.CharFilter(
        method='filter_event_date_range'
    )
    app_status = filters.CharFilter(
        method='filter_status'
    )

    def filter_date_create(self, queryset, name, value):
        if not value or value == '':
            return queryset
        return queryset.filter(
            date_create__date=datetime.datetime.strptime(value, "%d.%m.%Y").date()
        )

    def filter_event_type(self, queryset, name, value):
        if not value or value == '':
            return queryset
        events_ids = [event.object_id for event in Events.objects.filter(event_type__name=value)]
        return queryset.filter(event_id__in=events_ids)

    def filter_event_name(self, queryset, name, value):
        if not value or value == '':
            return queryset
        return queryset.filter(event__name__icontains=value)

    def filter_event_date_range(self, queryset, name, value):
        if not value or value == '':
            return queryset
        try:
            dates = value.split('-')
            date_start = datetime.datetime.strptime(
                dates[0],
                '%d.%m.%Y'
            )
            date_end = datetime.datetime.strptime(
                dates[1],
                '%d.%m.%Y'
            )
            event_ids=[
                event.object_id for event in Events.objects.filter(
                    Q(date_start__lte=date_start) &
                    Q(date_end__gte=date_end)
                )
            ]
            return queryset.filter(event_id__in=event_ids)
        except Exception:
            return queryset

    def filter_status(self, queryset, name, value):
        if not value or value == '':
            return queryset
        statuses = {value: key for key, value in APP_STATUSES}
        queryset = queryset.filter(status=statuses[value])
        return queryset

    class Meta:
        model = Apps
        fields = (
            'object_id',
            'date_create',
            'date_update',
            'event_type',
            'event_name',
            'event_date_range',
            'status'
        )
