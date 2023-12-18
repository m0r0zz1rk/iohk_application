from rest_framework import serializers

from apps.commons.serializers.pagination_serializer import PaginationSerializer
from apps.journals.models import Journal


class JournalSerializer(serializers.ModelSerializer):
    """Сериализация данных записей журнала"""
    rec_type = serializers.SerializerMethodField(
        label='Тип записи'
    )
    def get_rec_type(self, obj):
        return obj.get_rec_type_display()

    class Meta:
        model = Journal
        exclude = ('date_create', )


class JournalPaginationSerializer(PaginationSerializer):
    """Сериализация данных пагинационных записей журнала"""
    results = JournalSerializer(
        many=True,
        label='Записи журнала'
    )
