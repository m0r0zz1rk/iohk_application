import uuid
from typing import Optional

from django.apps import apps

from apps.applications.models import AppFields
from apps.events.utils.events import EventsUtils


class AppFieldsUtils:
    """Класс методов для работы с полями формы заявки на мероприятие"""

    @staticmethod
    def get_app_fields_for_event(event_id: uuid, app_type: str) -> Optional[AppFields]:
        """Получение списка полей для полученного типа заявки на мероприятие по его object_id"""
        if EventsUtils.get_event_by_object_id(event_id) is not None:
            qs = AppFields.objects.filter(event_id=event_id)
            if app_type == 'user_app':
                qs = qs.filter(user_app=True)
            else:
                qs = qs.filter(user_app=False)
            return qs.order_by('date_create')
        return None

    @staticmethod
    def get_app_fields_for_event_by_app_id(app_id: uuid, app_type: str) -> Optional[AppFields]:
        """Получение списка полей для полученного типа заявки на мероприятие по object_id заявки"""
        try:
            apps_model = apps.get_model('applications', 'Apps')
            event_id = apps_model.objects.get(object_id=app_id).event_id
            if EventsUtils.get_event_by_object_id(event_id) is not None:
                qs = AppFields.objects.filter(
                    event_id=event_id
                )
                if app_type == 'user_app':
                    qs = qs.filter(user_app=True)
                else:
                    qs = qs.filter(user_app=False)
                return qs.order_by('date_create')
            return None
        except Exception:
            return None

    @staticmethod
    def get_app_field_by_object_id(field_id: uuid) -> Optional[AppFields]:
        """Получение поля формы заявки по object_id"""
        try:
            return AppFields.objects.get(object_id=field_id)
        except Exception:
            return None

    @staticmethod
    def delete_app_field_by_object_id(field_id: uuid) -> Optional[str]:
        """Удаление поля по его object_id и возврат его имени"""
        try:
            field = AppFields.objects.get(object_id=field_id)
            name = field.name
            field.delete()
            return name
        except Exception:
            return None
