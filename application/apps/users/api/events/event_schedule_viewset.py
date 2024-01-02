from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.commons.permissions.is_users import IsUsers
from apps.events.serializers.events_schedule_serializer import EventsScheduleSerializer, \
    EventsSchedulePaginationSerializer
from apps.commons.consts.journals.journal_event_results import ERROR
from apps.commons.consts.journals.journal_rec_types import ADMINS
from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_auth import IsAuth
from apps.commons.utils.data_types.date import DateUtils
from apps.commons.utils.data_types.dict import DictUtils
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.commons.utils.django.rest import RestUtils
from apps.events.utils.events import EventsUtils
from apps.events.utils.events_schedule import EventsScheduleUtils
from apps.authen.utils.profile import ProfileUtils
from apps.journals.writer.journal_writer import JournalWriter


class EventScheduleViewSet(viewsets.ModelViewSet):
    """API для получения расписания мероприятия"""
    permission_classes = [IsAuth, IsUsers]
    queryset = EventsScheduleUtils.get_all_schedule()
    serializer_class = EventsScheduleSerializer
    pagination_class = CustomPagination

    journal = JournalWriter(ADMINS)
    ru = ResponseUtils()
    restu = RestUtils()
    du = DictUtils()
    dateu = DateUtils()
    pu = ProfileUtils()
    eu = EventsUtils()

    @swagger_auto_schema(
        tags=['Расписание мероприятия (ЛК пользователя)'],
        operation_description="Получение расписания мероприятия",
        responses={
            '400': 'Ошибка при получении расписания: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': EventsSchedulePaginationSerializer,
        }
    )
    def list(self, request, *args, **kwargs):
        """Получение расписания мероприятия"""
        try:
            queryset = EventsScheduleUtils.get_event_schedule(self.kwargs['event_id'])
            if queryset is not None:
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return self.ru.ok_response_dict(serializer.data)
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при получении расписания: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при получении расписания'
            )
