from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.authen.utils.profile import ProfileUtils
from apps.commons.consts.journals.journal_event_results import SUCCESS, ERROR
from apps.commons.consts.journals.journal_rec_types import EVENTS
from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_users import IsUsers
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.events.utils.events_schedule import EventsScheduleUtils
from apps.journals.writer.journal_writer import JournalWriter
from apps.users.serializers.schedule_serializer import ScheduleSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    """API для получения расписания занятий в ЛК пользователя"""
    permission_classes = [IsAuthenticated, IsUsers]
    queryset = EventsScheduleUtils.get_all_schedule()
    pagination_class = CustomPagination

    journal = JournalWriter(EVENTS)
    ru = ResponseUtils()
    pu = ProfileUtils()

    @swagger_auto_schema(
        tags=['Расписание занятий (ЛК пользователя)'],
        operation_description="Получение расписания занятий",
        responses={
            '400': 'Ошибка при получении расписания. Повторите попытку позже',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': ScheduleSerializer(many=True)
        }
    )
    def list(self, request, *args, **kwargs):
        """Получение расписания занятий"""
        try:
            profile = self.pu.get_profile_by_user_id(request.user.id)
            queryset = EventsScheduleUtils.get_user_schedule(profile.object_id)
            if queryset is None:
                return self.ru.ok_response_dict({})
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = ScheduleSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = ScheduleSerializer(queryset, many=True)
            self.journal.write(
                self.pu.get_display_name('django_user_id', request.user.id),
                SUCCESS,
                'Просмотр расписания занятий'
            )
            return self.ru.ok_response_dict(serializer.data)
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при получении расписания: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.sorry_try_again_response()
