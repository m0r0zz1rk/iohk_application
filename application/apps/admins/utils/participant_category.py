import uuid
from typing import Optional

from django.contrib.auth.models import Group

from apps.admins.models.guides.participant_categories import ParticipantCategories


class ParticipantCategoryUtils:
    """Класс методов для работы с категориями участников"""

    @staticmethod
    def get_participant_categories():
        """Получение всех категорий участников"""
        return ParticipantCategories.objects.all().order_by('name')

    @staticmethod
    def get_participant_category_by_object_id(object_id: uuid) -> Optional[ParticipantCategories]:
        """Получение категории участников по полученному object_id"""
        try:
            return ParticipantCategories.objects.get(object_id=object_id)
        except Exception:
            return None

    @staticmethod
    def delete_participant_category_by_object_id(object_id: uuid) -> Optional[str]:
        """Удаление категории участников по полученному object_id"""
        try:
            cat = ParticipantCategories.objects.get(object_id=object_id)
            name = cat.name
            cat.delete()
            return name
        except Exception:
            return None

    @staticmethod
    def get_group_id_by_name(name: str) -> Optional[int]:
        """Получение ID группы Django по полученному имени"""
        if Group.objects.filter(name=name).exists():
            return Group.objects.get(name=name).id
        return None

    @staticmethod
    def get_object_id_array_by_names(names: list) -> Optional[list]:
        """Получение списка object_id категорий по полученному списку имен"""
        try:
            res = []
            for name in names:
                res.append(ParticipantCategories.objects.get(name=name).object_id)
            return res
        except Exception:
            return None
