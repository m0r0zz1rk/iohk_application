import uuid
from typing import Optional

from apps.events.models.event_types import EventTypes


class EventsTypesUtils:
    """Класс для работы с типами мероприятий"""

    @staticmethod
    def get_events_type() -> dict:
        """Получение всех типов мероприятий"""
        return EventTypes.objects.all().order_by('name')

    @staticmethod
    def get_event_type_by_object_id(object_id: uuid) -> Optional[EventTypes]:
        """Получение типа мероприятия по полученному object_id"""
        try:
            return EventTypes.objects.get(object_id=object_id)
        except Exception:
            return None

    @staticmethod
    def get_event_type_object_id_by_name(name: str) -> Optional[uuid]:
        """Получение object_id типа мероприятия по его имени"""
        try:
            return EventTypes.objects.get(name=name).object_id
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
