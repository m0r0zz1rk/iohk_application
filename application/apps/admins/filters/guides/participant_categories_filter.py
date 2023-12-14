from django_filters import rest_framework as filters

from apps.admins.models.guides.participant_categories import ParticipantCategories


class ParticipantCategoriesFilter(filters.FilterSet):
    """Поля для фильтрации категорий участников"""
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    class Meta:
        model = ParticipantCategories
        fields = '__all__'
