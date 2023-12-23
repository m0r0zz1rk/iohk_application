from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.events.serializers.events_schedule_serializer import EventsScheduleSerializer, \
    EventsSchedulePaginationSerializer, EventScheduleModelSerializer, EventScheduleSaveSerializer
from apps.commons.consts.journals.journal_event_results import SUCCESS, ERROR
from apps.commons.consts.journals.journal_rec_types import ADMINS
from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_administrators import IsAdministrators
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


class EventsScheduleViewSet(viewsets.ModelViewSet):
    """API для работы с расписанием мероприятий в личном кабинете администратора"""
    permission_classes = [IsAuth, IsAdministrators]
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
        tags=['Расписание мероприятий (ЛК Администратора)'],
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
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            self.journal.write(
                self.pu.get_display_name('django_user_id', request.user.id),
                SUCCESS,
                f'Просмотр расписания мероприятия "'
                f'{EventsUtils.get_event_by_object_id(self.kwargs['event_id']).name}'
                f'"'
            )
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

    @swagger_auto_schema(
        tags=['Расписание мероприятий (ЛК Администратора)'],
        request_body=EventScheduleSaveSerializer,
        operation_description="Дополнение расписания мероприятия",
        responses={
            '400': 'Ошибка при дополнении расписания: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Расписание успешно дополнено'
        }
    )
    def save(self, request, *args, **kwargs):
        """Дополнение расписания мероприятия"""
        updated_data = request.data
        updated_data['event'] = self.kwargs['event_id']
        serialize = EventScheduleModelSerializer(data=updated_data)
        if serialize.is_valid(raise_exception=True):
            serialize.save()
            self.journal.write(
                self.pu.get_display_name('django_user_id', request.user.id),
                SUCCESS,
                f'Дополнено расписание мероприятия "'
                f'{EventsUtils.get_event_by_object_id(self.kwargs['event_id']).name}'
                f'"'
            )
            return self.ru.ok_response('Расписание успешно дополнено')
        else:

            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при дополнении расписания мероприятия: {serialize.errors}'
            )
            return self.ru.bad_request_response(serialize.errors)

    @swagger_auto_schema(
        tags=['Расписание мероприятий (ЛК Администратора)'],
        request_body=EventScheduleSaveSerializer,
        operation_description="Изменение расписания мероприятия",
        responses={
            '400': 'Ошибка при изменении расписания мероприятия: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Расписание мероприятия успешно изменено'
        }
    )
    def edit(self, request, *args, **kwargs):
        """Изменение расписания мероприятия"""
        sched = EventsScheduleUtils.get_schedule_by_object_ud(self.kwargs['schedule_id'])
        serialize = EventScheduleSaveSerializer(sched, data=request.data, partial=True)
        if serialize.is_valid(raise_exception=True):
            serialize.save()
            self.journal.write(
                self.pu.get_display_name('django_user_id', request.user.id),
                SUCCESS,
                f'Изменено расписание мероприятия "'
                f'{EventsUtils.get_event_by_object_id(sched.event_id).name}'
                f'"'
            )
            return self.ru.ok_response('Расписание успешно изменено')
        else:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при изменении расписания мероприятия: {serialize.errors}'
            )
            return self.ru.bad_request_response(serialize.errors)

    @swagger_auto_schema(
        tags=['Расписание мероприятий (ЛК Администратора)'],
        operation_description="Удаление части расписания мероприятия",
        responses={
            '400': 'Ошибка при удалении части расписания мероприятия: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Расписание успешно изменено'
        }
    )
    def delete(self, request, *args, **kwargs):
        try:
            sched = EventsScheduleUtils.get_schedule_by_object_ud(self.kwargs['schedule_id'])
            sched.delete()
            self.journal.write(
                self.pu.get_display_name('django_user_id', request.user.id),
                SUCCESS,
                f'Удалена часть расписания с темой "{sched.theme}" мероприятия "{sched.event.name}"'
            )
            return self.ru.ok_response('Расписание успешно изменено')
        except Exception:
            error = ExceptionHandling.get_traceback()
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при удалении части расписания мероприятия: {error}'
            )
            return self.ru.bad_request_response(error)
