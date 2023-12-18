from django_filters import rest_framework as filters

from apps.events.models.event_types import EventTypes


class EventsTypesFilter(filters.FilterSet):
    """Поля для фильтрации типов мероприятий"""
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    class Meta:
        model = EventTypes
        fields = '__all__'
