import uuid
from typing import Optional

from django.apps import apps

from apps.events.models import EventsAppsRequired


class EventsAppsRequiredUtils:
    """Класс методов для работы с записями необходимости форм заявок для мероприятий"""

    @staticmethod
    def get_all_apps_required():
        """Получение всех записей о необходимости форм заявок для мероприятий"""
        return EventsAppsRequired.objects.all()

    @staticmethod
    def get_apps_required_for_event(event_id: uuid) -> Optional[EventsAppsRequired]:
        """Получение записи о необходимости форм заявок для мероприятия по его object_id"""
        if EventsAppsRequired.objects.filter(event_id=event_id).exists():
            return EventsAppsRequired.objects.get(event_id=event_id)
        return None

    @staticmethod
    def get_apps_required_for_event_by_app_id(app_id: uuid) -> Optional[EventsAppsRequired]:
        """Получение записи о необходимости форм заявок для мероприятия по object_id заявки"""
        apps_model = apps.get_model('applications', 'Apps')
        try:
            if EventsAppsRequired.objects.filter(event_id=apps_model.objects.get(object_id=app_id).event_id).exists():
                return EventsAppsRequired.objects.get(event_id=apps_model.objects.get(object_id=app_id).event_id)
            return None
        except Exception:
            return None

    @staticmethod
    def change_app_required_for_event(data: dict) -> bool:
        """Изменение необходимости формы заявки для мероприятия"""
        try:
            update_data = {
                data['type']: data['value']
            }
            EventsAppsRequired.objects.filter(event_id=data['event_id']).update(**update_data)
            return True
        except Exception:
            return False
