import uuid
from typing import Optional

from apps.admins.models.guides.event_types import EventTypes


class EventsTypesUtils:
    """Класс для работы с типами мероприятий"""

    @staticmethod
    def get_events_type() -> dict:
        """Получение всех типов мероприятий"""
        return EventTypes.objects.all().order_by('name')

    @staticmethod
    def get_events_types_count() -> int:
        """Получение количества всех типов мероприятий"""
        return EventTypes.objects.count()

    @staticmethod
    def get_event_type_by_object_id(object_id: uuid) -> Optional[EventTypes]:
        """Получение типа мероприятия по полученному object_id"""
        try:
            return EventTypes.objects.get(object_id=object_id)
        except Exception:
            return None

    @staticmethod
    def delete_event_type_by_object_id(object_id: uuid) -> Optional[str]:
        """Удаление типа мероприятия по полученному object_id"""
        try:
            type = EventTypes.objects.get(object_id=object_id)
            name = type.name
            type.delete()
            return name
        except Exception:
            return None
