from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.events.filters.events_filter import EventsFilter
from apps.events.serializers.events_serializer import EventsPaginationSerializer, EventsSerializer, EventSaveSerializer, \
    EventModelSerializer, EventGetSerializer
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
from apps.events.utils.events_type import EventsTypesUtils
from apps.admins.utils.participant_category import ParticipantCategoryUtils
from apps.authen.utils.profile import ProfileUtils
from apps.journals.writer.journal_writer import JournalWriter


class EventsViewSet(viewsets.ModelViewSet):
    """API для работы с мероприятиями в личном кабинете администратора"""
    permission_classes = [IsAuth, IsAdministrators]
    queryset = EventsUtils.get_all_events()
    serializer_class = EventsSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend,]
    filterset_class = EventsFilter

    journal = JournalWriter(ADMINS)
    ru = ResponseUtils()
    restu = RestUtils()
    du = DictUtils()
    dateu = DateUtils()
    pu = ProfileUtils()
    eu = EventsUtils()

    @swagger_auto_schema(
        tags=['Мероприятия (ЛК Администратора)'],
        operation_description="Получение мероприятий",
        responses={
            '400': 'Ошибка при получении списка мероприятий: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': EventsPaginationSerializer,
        }
    )
    def list(self, request, *args, **kwargs):
        """Получение мероприятий"""
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            self.journal.write(
                self.pu.get_display_name('django_user_id', request.user.id),
                SUCCESS,
                'Просмотр мероприятий'
            )
            return self.ru.ok_response_dict(serializer.data)
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при получении мероприятий: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при получении мероприятий'
            )

    @swagger_auto_schema(
        tags=['Мероприятия (ЛК Администратора)'],
        operation_description="Получение мероприятия",
        responses={
            '400': 'Ошибка при получении мероприятия: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': EventsSerializer,
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """Получение мероприятия"""
        try:
            event = EventsUtils.get_event_by_object_id(self.kwargs['event_id'])
            serializer = self.get_serializer(event)
            self.journal.write(
                self.pu.get_display_name('django_user_id', request.user.id),
                SUCCESS,
                'Просмотр мероприятия'
            )
            return self.ru.ok_response_dict(serializer.data)
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при получении мероприятия: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при получении мероприятия'
            )

    @swagger_auto_schema(
        tags=['Мероприятия (ЛК Администратора)'],
        request_body=EventSaveSerializer,
        operation_description="Добавление мероприятия",
        responses={
            '400': 'Ошибка при добавлении типа мероприятий: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Мероприятие успешно добавлено'
        }
    )
    def save(self, request, *args, **kwargs):
        """Добавление мероприятия"""
        serialize = EventSaveSerializer(data=request.data)
        if serialize.is_valid(raise_exception=True):
            if self.dateu.check_cross_and_second_after_first_date_ranges(
                serialize.data['app_date_range'],
                serialize.data['date_range']
            ):
                self.journal.write(
                    'Система',
                    ERROR,
                    f'Ошибка при добавлении мероприятия: '
                    f'Некорректные временные интервалы'
                )
                return self.ru.bad_request_response('Подача заявок должна завершиться'
                                                        ' раньше сроков проведения мероприятия')
            apps_dates = self.dateu.split_date_range(serialize.data['app_date_range'])
            event_dates = self.dateu.split_date_range(serialize.data['date_range'])
            event_data = {
                'app_date_start': apps_dates[0],
                'app_date_end': apps_dates[1],
                'date_start': event_dates[0],
                'date_end': event_dates[1],
            }
            for key, value in serialize.data.items():
                if key not in ['app_date_range', 'date_range']:
                    if key == 'event_type':
                        event_data['event_type_id'] = EventsTypesUtils.get_event_type_object_id_by_name(value)
                    else:
                        event_data[key] = value
            if self.eu.create_event_from_data(event_data):
                self.journal.write(
                    self.pu.get_display_name('django_user_id', request.user.id),
                    SUCCESS,
                    f'Добавлено новое мероприятие: '
                    f'{self.du.get_str_value_in_dict_by_key(
                        'name',
                        request.data
                    )}'
                )
                return self.ru.ok_response('Мероприятие успешно добавлено')
        else:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при добавлении мероприятия: {serialize.errors}'
            )
            return self.ru.bad_request_response(serialize.errors)

    @swagger_auto_schema(
        tags=['Мероприятия (ЛК Администратора)'],
        request_body=EventSaveSerializer,
        operation_description="Изменение базовой информации о мероприятии",
        responses={
            '400': 'Ошибка при изменении базовой информации о мероприятии: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Базовая информация о мероприятии успешно изменена'
        }
    )
    def edit(self, request, *args, **kwargs):
        """Изменение базовой информации о мероприятии"""
        serialize = EventSaveSerializer(data=request.data)
        if serialize.is_valid(raise_exception=True):
            try:
                if self.dateu.check_cross_and_second_after_first_date_ranges(
                        serialize.data['app_date_range'],
                        serialize.data['date_range']
                ):
                    self.journal.write(
                        'Система',
                        ERROR,
                        f'Ошибка при добавлении мероприятия: '
                        f'Некорректные временные интервалы'
                    )
                    return self.ru.bad_request_response('Сроки подачи заявок должны быть окончены'
                                                        ' раньше сроков проведения мероприятия')
                event = EventsUtils.get_event_by_object_id(self.kwargs['object_id'])
                apps_dates = self.dateu.split_date_range(serialize.data['app_date_range'])
                event_dates = self.dateu.split_date_range(serialize.data['date_range'])
                event_data = {
                    'app_date_start': apps_dates[0].date(),
                    'app_date_end': apps_dates[1].date(),
                    'date_start': event_dates[0].date(),
                    'date_end': event_dates[1].date(),
                    'categories': ParticipantCategoryUtils.get_object_id_array_by_names(serialize.data['categories'])
                }
                for key, value in serialize.data.items():
                    if key not in ['app_date_range', 'date_range', 'categories']:
                        if key == 'event_type':
                            event_data['event_type_id'] = EventsTypesUtils.get_event_type_object_id_by_name(value)
                        else:
                            event_data[key] = value
                save_serialize = EventModelSerializer(event, data=event_data, partial=True)
                if save_serialize.is_valid(raise_exception=True):
                    save_serialize.save()
                    self.journal.write(
                        self.pu.get_display_name('django_user_id', request.user.id),
                        SUCCESS,
                        f'Изменена базовая информация мероприятия: '
                        f'{event_data['name']}'
                    )
                    return self.ru.ok_response('Информация о мероприятии успешно изменена')
                else:
                    self.journal.write(
                        'Система',
                        ERROR,
                        f'Ошибка при изменении базовой информации о мероприятии: {serialize.errors}'
                    )
                    return self.ru.bad_request_response(serialize.errors)
            except Exception:
                error = ExceptionHandling.get_traceback()
                self.journal.write(
                    'Система',
                    ERROR,
                    f'Ошибка при изменении базовой информации о мероприятии: {error}'
                )
                return self.ru.bad_request_response(error)
        else:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при изменении базовой информации о мероприятии: {serialize.errors}'
            )
            return self.ru.bad_request_response(serialize.errors)

    @swagger_auto_schema(
        tags=['Мероприятия (ЛК Администратора)'],
        operation_description="Удаление мероприятия",
        responses={
            '400': 'Ошибка при удалении мероприятия: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Мероприятие успешно удалено'
        }
    )
    def delete(self, request, *args, **kwargs):
        try:
            name = EventsUtils.delete_event_by_object_id(self.kwargs['object_id'])
            self.journal.write(
                self.pu.get_display_name('django_user_id', request.user.id),
                SUCCESS,
                f'Удалено мероприятие: {name}'
            )
            return self.ru.ok_response('Мероприятие успешно удалено')
        except Exception:
            error = ExceptionHandling.get_traceback()
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при удалении мероприятия: {error}'
            )
            return self.ru.bad_request_response(error)
