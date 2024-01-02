import uuid
from typing import Optional

from apps.applications.models import Apps


class AppsUtils:
    """Класс методов для работы с заявками"""

    @staticmethod
    def get_all_apps():
        """Получение всех заявок по всем мероприятиям"""
        return Apps.objects.all()

    @staticmethod
    def get_app_by_profile_and_event_id(profile_id: uuid, event_id: uuid) -> Optional[Apps]:
        """Получение заявки по object_id"""
        try:
            return Apps.objects.filter(profile_id=profile_id).get(event_id=event_id)
        except Exception:
            return None

    @staticmethod
    def check_event_app_for_user(profile_id: uuid, event_id: uuid) -> bool:
        """Проверка на наличие заявки у пользователя на участие в мероприятии"""
        try:
            return Apps.objects.filter(profile_id=profile_id).filter(event_id=event_id).exists()
        except Exception:
            return False
