import datetime
import uuid
from typing import Optional

from django.contrib.auth.models import Group
from django.db.models import Q

from apps.admins.utils.participant_category import ParticipantCategoryUtils
from apps.commons.consts.events.event_statuses import PUBLISHED
from apps.events.models.events import Events


class EventsUtils:
    """Класс методов для работы с мероприятиями"""

    @staticmethod
    def get_all_events():
        """Получение всех мероприятий"""
        return Events.objects.all().order_by('-date_start')

    @staticmethod
    def get_events_by_event_type_and_group(event_type: str, user_group: str) -> Optional[Events]:
        """Получение списка мероприятий по полученному названию типа мероприятия"""
        try:
            type_events = Events.objects.filter(event_type__name=event_type)
            criteria1 = Q(app_date_start__lte=datetime.date.today())
            criteria2 = Q(app_date_end__gte=datetime.date.today())
            return (type_events.filter(event_status=PUBLISHED).
                    filter(criteria1 & criteria2).
                    filter(categories__group__name=user_group).
                    order_by('app_date_start'))
        except Exception:
            return None

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
