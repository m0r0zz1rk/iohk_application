import datetime
import uuid
from typing import Optional

from django.apps import apps
from django.db.models import Q
from django.utils import timezone

from apps.commons.consts.apps.app_statuses import ACCEPTED
from apps.events.models import EventsSchedule


class EventsScheduleUtils:
    """Класс методов для работы с расписанием мероприятий"""

    @staticmethod
    def get_all_schedule():
        """Получение всех расписаний мероприятий"""
        return EventsSchedule.objects.all().order_by('start')

    @staticmethod
    def get_event_schedule(event_id):
        """Получение расписания по object_id мероприятия"""
        if EventsSchedule.objects.filter(event_id=event_id).exists():
            return EventsSchedule.objects.filter(event_id=event_id).all().order_by('start')
        return None

    @staticmethod
    def get_schedule_by_object_ud(schedule_id):
        """Получение расписания по object_id"""
        if EventsSchedule.objects.filter(object_id=schedule_id).exists():
            return EventsSchedule.objects.get(object_id=schedule_id)
        return None

    @staticmethod
    def get_user_schedule(profile_id: uuid) -> Optional[EventsSchedule]:
        """Получение расписания ближайших занятий для ЛК пользователя"""
        try:
            apps_model = apps.get_model('applications', 'Apps')
            user_apps = apps_model.objects.filter(profile_id=profile_id)
            if user_apps.count() > 0:
                event_ids = [app.event_id for app in user_apps.filter(status=ACCEPTED)]
                tz = timezone.get_current_timezone()
                res = (EventsSchedule.objects.filter(event_id__in=event_ids).
                       filter(
                            Q(start__gte=datetime.datetime.now().replace(tzinfo=tz)) &
                            Q(end__gte=datetime.datetime.now().replace(tzinfo=tz))
                )
                )
                print(res)
                return res
            return None
        except Exception:
            return None

    @staticmethod
    def check_part_cross_to_another(part_id: uuid) -> bool:
        """Проверка на пересечение времени проведения части мероприятия с другими частями"""
        try:
            curr_part = EventsSchedule.objects.get(object_id=part_id)
            parts = EventsSchedule.objects.filter(event_id=curr_part.event_id)
            if parts.count() != 0:
                flag = False
                for part in parts:
                    if part.object_id != curr_part.object_id:
                        if (part.start <= curr_part.start <= part.end or
                                part.start <= curr_part.end <= part.end):
                            flag = True
                            break
                return flag
            return False
        except Exception:
            return True
