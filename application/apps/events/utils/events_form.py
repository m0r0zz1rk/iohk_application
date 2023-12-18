import uuid
from typing import Optional

from apps.events.models.event_forms import EventForms


class EventsFormsUtils:
    """Класс для работы с формами проведения мероприятий"""

    @staticmethod
    def get_events_forms() -> dict:
        """Получение всех форм проведения мероприятий"""
        return EventForms.objects.all().order_by('name')

    @staticmethod
    def get_event_form_by_object_id(object_id: uuid) -> Optional[EventForms]:
        """Получение формы проведения мероприятия по полученному object_id"""
        try:
            return EventForms.objects.get(object_id=object_id)
        except Exception:
            return None

    @staticmethod
    def delete_event_form_by_object_id(object_id: uuid) -> Optional[str]:
        """Удаление формы проведения мероприятия по полученному object_id"""
        try:
            form = EventForms.objects.get(object_id=object_id)
            name = form.name
            form.delete()
            return name
        except Exception:
            return None
