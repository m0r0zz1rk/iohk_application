from django.contrib.auth.models import Group
from django_filters import rest_framework as filters

from apps.admins.models.guides.participant_categories import ParticipantCategories


class ParticipantCategoriesFilter(filters.FilterSet):
    """Поля для фильтрации категорий участников"""
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    group = filters.CharFilter(
        method='filter_role'
    )

    def filter_role(self, queryset, name, value):
        django_group = Group.objects.get(name=value)
        queryset = queryset.filter(group_id=django_group.id)
        return queryset

    class Meta:
        model = ParticipantCategories
        fields = '__all__'
