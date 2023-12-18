import uuid
from typing import Optional

from apps.events.models import EventsInformation


class EventsInformationUtils:
    """Класс методов для работы с информационными сообщениями"""

    @staticmethod
    def get_all_information():
        """Получение всех информационных сообщений"""
        return EventsInformation.objects.all()

    @staticmethod
    def get_event_information_by_event_id(event_id: uuid) -> Optional[EventsInformation]:
        """Получение информационного сообщения по object_id мероприятия"""
        try:
            return EventsInformation.objects.get(event_id=event_id)
        except Exception:
            return None
