from rest_framework import serializers

from apps.admins.models.guides.participant_categories import ParticipantCategories
from apps.commons.serializers.pagination_serializer import PaginationSerializer


class ParticipantCategoriesSerializer(serializers.ModelSerializer):
    """Сериализация модели категорий участников"""
    group = serializers.SerializerMethodField(
        label='Роль пользователей'
    )

    def get_group(self, obj):
        if obj.group is None:
            return '-'
        return obj.group.name

    class Meta:
        model = ParticipantCategories
        fields = ('object_id', 'name', 'group')


class ParticipantCategoriesPaginationSerializer(PaginationSerializer):
    """Сериализация данных при пагинации категорий участников"""
    results = ParticipantCategoriesSerializer(many=True)


class ParticipantCategoriesSaveSerializer(serializers.ModelSerializer):
    """Сериализация данных при добавлении новой категории участников"""

    class Meta:
        model = ParticipantCategories
        fields = ('name', 'group')
