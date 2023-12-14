from django_filters import rest_framework as filters

from apps.admins.models.guides.event_forms import EventForms


class EventsFormsFilter(filters.FilterSet):
    """Поля для фильтрации форм проведения мероприятий"""
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    class Meta:
        model = EventForms
        fields = '__all__'
