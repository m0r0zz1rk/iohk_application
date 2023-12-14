from rest_framework import serializers

from apps.admins.models.guides.participant_categories import ParticipantCategories
from apps.commons.pagination_serializer import PaginationSerializer


class ParticipantCategoriesSerializer(serializers.ModelSerializer):
    """Сериализация модели категорий участников"""
    class Meta:
        model = ParticipantCategories
        fields = ('object_id', 'name')


class ParticipantCategoriesPaginationSerializer(PaginationSerializer):
    """Сериализация данных при пагинации категорий участников"""
    results = ParticipantCategoriesSerializer(many=True)


class ParticipantCategoriesSaveSerializer(serializers.ModelSerializer):
    """Сериализация данных при добавлении новой категории участников"""
    class Meta:
        model = ParticipantCategories
        fields = ('name',)
