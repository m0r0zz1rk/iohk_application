import uuid

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
