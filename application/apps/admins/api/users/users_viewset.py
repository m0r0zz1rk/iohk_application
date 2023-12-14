from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.admins.filters.users.users_filter import UsersFilter
from apps.admins.serializers.guides.events_types_serializer import EventsTypeSerializer, \
    EventsTypesSaveSerializer
from apps.admins.serializers.users.users_serializer import UsersSerializer, UsersPaginationSerializer
from apps.commons.consts.journals.journal_event_results import SUCCESS, ERROR
from apps.commons.consts.journals.journal_rec_types import ADMINS
from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.permissions.is_auth import IsAuth
from apps.commons.utils.data_types.dict import DictUtils
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.commons.utils.models.events_type import EventsTypesUtils
from apps.commons.utils.models.profile import ProfileUtils
from apps.journals.writer.journal_writer import JournalWriter


class UsersViewSet(viewsets.ModelViewSet):
    """API для работы с пользователями"""
    permission_classes = [IsAuth, IsAdministrators]
    queryset = ProfileUtils.get_all_profiles()
    serializer_class = UsersSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend,]
    filterset_class = UsersFilter

    journal = JournalWriter(ADMINS)
    ru = ResponseUtils()
    du = DictUtils()
    pu = ProfileUtils()

    @swagger_auto_schema(
        tags=['Администраторы_Пользователи'],
        operation_description="Получение пользователей",
        responses={
            '400': 'Ошибка при получении списка пользователей: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': UsersPaginationSerializer,
        }
    )
    def list(self, request, *args, **kwargs):
        """Получение типов мероприятий"""
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
                'Просмотр пользователей'
            )
            return self.ru.ok_response_dict(serializer.data)
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при получении пользователей: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при получении пользователей'
            )

    @swagger_auto_schema(
        tags=['Типы мероприятий'],
        request_body=EventsTypesSaveSerializer,
        operation_description="Добавление типа мероприятия",
        responses={
            '400': 'Ошибка при добавлении типа мероприятий: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Тип мероприятия успешно добавлен'
        }
    )
    def save(self, request, *args, **kwargs):
        serialize = EventsTypeSerializer(data=request.data)
        if serialize.is_valid(raise_exception=True):
            serialize.save()
            self.journal.write(
                self.pu.get_display_name('django_user_id', request.user.id),
                SUCCESS,
                f'Добавлен новый тип мероприятий: '
                f'{self.du.get_str_value_in_dict_by_key(
                    'name',
                    request.data
                )}'
            )
            return self.ru.ok_response('Тип мероприятия успешно добавлен')
        else:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при добавлении типа мероприятия: {serialize.errors}'
            )
            return self.ru.bad_request_response(serialize.errors)

    @swagger_auto_schema(
        tags=['Типы мероприятий'],
        request_body=EventsTypesSaveSerializer,
        operation_description="Изменение типа мероприятия",
        responses={
            '400': 'Ошибка при изменении типа мероприятий: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Тип мероприятия успешно изменен'
        }
    )
    def edit(self, request, *args, **kwargs):
        try:
            event_type = EventsTypesUtils.get_event_type_by_object_id(self.kwargs['object_id'])
            serialize = EventsTypeSerializer(event_type, data=request.data, partial=True)
            if serialize.is_valid(raise_exception=True):
                serialize.save()
                self.journal.write(
                    self.pu.get_display_name('django_user_id', request.user.id),
                    SUCCESS,
                    f'Изменен тип мероприятий: '
                    f'{DictUtils().get_str_value_in_dict_by_key(
                        'name',
                        request.data
                    )}'
                )
                return self.ru.ok_response('Тип мероприятия успешно изменен')
            else:
                self.journal.write(
                    'Система',
                    ERROR,
                    f'Ошибка при изменении типа мероприятия: {serialize.errors}'
                )
                return self.ru.bad_request_response(serialize.errors)
        except Exception:
            error = ExceptionHandling.get_traceback()
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при изменении типа мероприятия: {error}'
            )
            return self.ru.bad_request_response(error)

    @swagger_auto_schema(
        tags=['Типы мероприятий'],
        operation_description="Удаление типа мероприятия",
        responses={
            '400': 'Ошибка при удалении типа мероприятий: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Тип мероприятия успешно удален'
        }
    )
    def delete(self, request, *args, **kwargs):
        try:
            name = EventsTypesUtils.delete_event_type_by_object_id(self.kwargs['object_id'])
            self.journal.write(
                self.pu.get_display_name('django_user_id', request.user.id),
                SUCCESS,
                f'Удален тип мероприятий: {name}'
            )
            return self.ru.ok_response('Тип мероприятия успешно удален')
        except Exception:
            error = ExceptionHandling.get_traceback()
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при удалении типа мероприятия: {error}'
            )
            return self.ru.bad_request_response(error)
