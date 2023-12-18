import uuid
from typing import Optional

from apps.admins.utils.participant_category import ParticipantCategoryUtils
from apps.events.models.events import Events


class EventsUtils:
    """Класс методов для работы с мероприятиями"""

    @staticmethod
    def get_all_events():
        """Получение всех мероприятий"""
        return Events.objects.all().order_by('-date_start')

    @staticmethod
    def create_event_from_data(data: dict) -> bool:
        """Создание мероприятия на основе полученной data"""
        try:
            cats = data['categories']
            data.pop('categories')
            new_event = Events.objects.create(**data)
            for category in ParticipantCategoryUtils.get_object_id_array_by_names(cats):
                new_event.categories.add(category)
            return True
        except Exception:
            return False

    @staticmethod
    def get_event_by_object_id(object_id: uuid) -> Optional[Events]:
        """Получение мероприятия по object_id"""
        try:
            return Events.objects.get(object_id=object_id)
        except Exception:
            return None

    @staticmethod
    def delete_event_by_object_id(object_id: uuid) -> Optional[str]:
        """Удаление мероприятия, получение наименования"""
        try:
            name = Events.objects.get(object_id=object_id).name
            Events.objects.get(object_id=object_id).delete()
            return name
        except Exception:
            return None
