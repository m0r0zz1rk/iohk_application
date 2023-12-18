from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.admins.filters.guides.events_forms_filter import EventsFormsFilter
from apps.admins.serializers.guides.events_forms_serializer import EventsFormSerializer, EventsFormPaginationSerializer, \
    EventsFormSaveSerializer
from apps.commons.consts.journals.journal_event_results import SUCCESS, ERROR
from apps.commons.consts.journals.journal_rec_types import ADMINS
from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.permissions.is_auth import IsAuth
from apps.commons.utils.data_types.dict import DictUtils
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.events.utils.events_form import EventsFormsUtils
from apps.authen.utils.profile import ProfileUtils
from apps.journals.writer.journal_writer import JournalWriter


class EventsFormsViewSet(viewsets.ModelViewSet):
    """API для работы с формами проведения мероприятий"""
    permission_classes = [IsAuth, IsAdministrators]
    queryset = EventsFormsUtils.get_events_forms()
    serializer_class = EventsFormSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend,]
    filterset_class = EventsFormsFilter

    journal = JournalWriter(ADMINS)
    ru = ResponseUtils()
    du = DictUtils()
    pu = ProfileUtils()

    @swagger_auto_schema(
        tags=['Формы проведения мероприятий'],
        operation_description="Получение форм проведения мероприятий",
        responses={
            '400': 'Ошибка при получении списка форм проведения мероприятий: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': EventsFormPaginationSerializer,
        }
    )
    def list(self, request, *args, **kwargs):
        """Получение форм проведения мероприятий"""
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
                'Просмотр форм проведения мероприятий'
            )
            return self.ru.ok_response_dict(serializer.data)
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при получении форм проведения мероприятий: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при получении форм проведения мероприятий'
            )

    @swagger_auto_schema(
        tags=['Формы проведения мероприятий'],
        request_body=EventsFormSaveSerializer,
        operation_description="Добавление формы проведения мероприятия",
        responses={
            '400': 'Ошибка при добавлении формы проведения мероприятий: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Форма проведения мероприятия успешно добавлена'
        }
    )
    def save(self, request, *args, **kwargs):
        serialize = EventsFormSaveSerializer(data=request.data)
        if serialize.is_valid(raise_exception=True):
            serialize.save()
            self.journal.write(
                self.pu.get_display_name('django_user_id', request.user.id),
                SUCCESS,
                f'Добавлен новая форма проведения мероприятий: '
                f'{self.du.get_str_value_in_dict_by_key(
                    'name',
                    request.data
                )}'
            )
            return self.ru.ok_response('Форма проведения мероприятия успешно добавлена')
        else:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при добавлении форм проведения мероприятия: {serialize.errors}'
            )
            return self.ru.bad_request_response(serialize.errors)

    @swagger_auto_schema(
        tags=['Формы проведения мероприятий'],
        request_body=EventsFormSaveSerializer,
        operation_description="Изменение формы проведения мероприятия",
        responses={
            '400': 'Ошибка при изменении формы проведения мероприятий: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Форма проведения успешно изменена'
        }
    )
    def edit(self, request, *args, **kwargs):
        try:
            event_form = EventsFormsUtils.get_event_form_by_object_id(self.kwargs['object_id'])
            serialize = EventsFormSerializer(event_form, data=request.data, partial=True)
            if serialize.is_valid(raise_exception=True):
                serialize.save()
                self.journal.write(
                    self.pu.get_display_name('django_user_id', request.user.id),
                    SUCCESS,
                    f'Изменена форма проведения мероприятий: '
                    f'{DictUtils().get_str_value_in_dict_by_key(
                        'name',
                        request.data
                    )}'
                )
                return self.ru.ok_response('Форма проведения мероприятия успешно изменена')
            else:
                self.journal.write(
                    'Система',
                    ERROR,
                    f'Ошибка при изменении формы проведения мероприятия: {serialize.errors}'
                )
                return self.ru.bad_request_response(serialize.errors)
        except Exception:
            error = ExceptionHandling.get_traceback()
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при изменении формы проведения мероприятия: {error}'
            )
            return self.ru.bad_request_response(error)

    @swagger_auto_schema(
        tags=['Формы проведения мероприятий'],
        operation_description="Удаление формы проведения мероприятия",
        responses={
            '400': 'Ошибка при удалении формы проведения мероприятий: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Форма проведения мероприятия успешно удалена'
        }
    )
    def delete(self, request, *args, **kwargs):
        try:
            name = EventsFormsUtils.delete_event_form_by_object_id(self.kwargs['object_id'])
            self.journal.write(
                self.pu.get_display_name('django_user_id', request.user.id),
                SUCCESS,
                f'Удалена форма проведения мероприятий: {name}'
            )
            return self.ru.ok_response('Форма проведения мероприятия успешно удален')
        except Exception:
            error = ExceptionHandling.get_traceback()
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при удалении формы проведения мероприятия: {error}'
            )
            return self.ru.bad_request_response(error)
