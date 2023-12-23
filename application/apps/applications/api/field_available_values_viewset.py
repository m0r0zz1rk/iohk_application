from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.applications.serializers.field_available_values_serializer import FieldAvailableValuesSerializer, \
    FieldAvailableValueSaveSerializer, FieldAvailableValueGiveSerializer
from apps.applications.utils.app_fields import AppFieldsUtils
from apps.applications.utils.field_available_values import FieldAvailableValuesUtils
from apps.commons.consts.journals.journal_event_results import SUCCESS, ERROR
from apps.commons.consts.journals.journal_rec_types import APPLICATIONS
from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.permissions.is_auth import IsAuth
from apps.commons.utils.data_types.date import DateUtils
from apps.commons.utils.data_types.dict import DictUtils
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.commons.utils.django.rest import RestUtils
from apps.events.utils.events import EventsUtils
from apps.authen.utils.profile import ProfileUtils
from apps.journals.writer.journal_writer import JournalWriter


class FieldAvailableValuesViewSet(viewsets.ModelViewSet):
    """API для работы с возможными значения поля заявки"""
    permission_classes = [IsAuth, IsAdministrators]
    queryset = FieldAvailableValuesUtils.get_all_available_values()
    pagination_class = CustomPagination
    serializer_class = FieldAvailableValuesSerializer

    journal = JournalWriter(APPLICATIONS)
    ru = ResponseUtils()
    restu = RestUtils()
    du = DictUtils()
    dateu = DateUtils()
    pu = ProfileUtils()
    eu = EventsUtils()

    @swagger_auto_schema(
        tags=['Возможные значения поля заявки'],
        operation_description="Получение списка возможных значений поля",
        responses={
            '400': 'Ошибка при получении списка: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '200': FieldAvailableValuesSerializer(many=True),
        }
    )
    def list(self, request, *args, **kwargs):
        """Получение списка возможных значений поля"""
        try:
            queryset = FieldAvailableValuesUtils.get_available_values_for_field(self.kwargs['field_id'])
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            self.journal.write(
                self.pu.get_display_name('django_user_id', request.user.id),
                SUCCESS,
                f'Получение списка возможных значений поля "{
                    AppFieldsUtils.get_app_field_by_object_id(self.kwargs['field_id']).name
                }"'
            )
            return self.ru.ok_response_dict(serializer.data)
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при получении списка: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при получении списка возможных значений поля'
            )

    @swagger_auto_schema(
        tags=['Возможные значения поля заявки'],
        request_body=FieldAvailableValueGiveSerializer,
        operation_description="Добавление возможного значения поля",
        responses={
            '400': 'Ошибка при добавлении возможного значения: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Возможное значение успешно добавлено'
        }
    )
    def save(self, request, *args, **kwargs):
        data = {
            **request.data,
            'field': self.kwargs['field_id']
        }
        serialize = FieldAvailableValueSaveSerializer(data=data)
        if serialize.is_valid(raise_exception=True):
            serialize.save()
            self.journal.write(
                self.pu.get_display_name('django_user_id', request.user.id),
                SUCCESS,
                f'Добавлен новое возможное значение "'
                f'{self.du.get_str_value_in_dict_by_key(
                    'option',
                    request.data
                )}" для поля "{
                    AppFieldsUtils.get_app_field_by_object_id(self.kwargs['field_id']).name
                }"'
            )
            return self.ru.ok_response('Возможное значение успешно добавлено')
        else:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при добавлении возможного значения: {serialize.errors}'
            )
            return self.ru.bad_request_response(serialize.errors)

    @swagger_auto_schema(
        tags=['Возможные значения поля заявки'],
        request_body=FieldAvailableValueGiveSerializer,
        operation_description="Изменение возможного значения поля",
        responses={
            '400': 'Ошибка при изменении возможного значения поля: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Возможное значение успешно изменено'
        }
    )
    def edit(self, request, *args, **kwargs):
        try:
            value = FieldAvailableValuesUtils.get_available_value_by_object_id(self.kwargs['value_id'])
            serialize = FieldAvailableValueSaveSerializer(
                value,
                data=request.data,
                partial=True
            )
            if serialize.is_valid(raise_exception=True):
                serialize.save()
                self.journal.write(
                    self.pu.get_display_name('django_user_id', request.user.id),
                    SUCCESS,
                    f'Изменен возможное значение "{
                        DictUtils().get_str_value_in_dict_by_key(
                        'option',
                        request.data
                    )
                    }" для поля "{
                        value.field.name
                    }"'
                )
                return self.ru.ok_response('Возможное значение успешно изменено')
            else:
                self.journal.write(
                    'Система',
                    ERROR,
                    f'Ошибка при изменении возможного значения поля: {serialize.errors}'
                )
                return self.ru.bad_request_response(serialize.errors)
        except Exception:
            error = ExceptionHandling.get_traceback()
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при изменении возможного значения поля: {error}'
            )
            return self.ru.bad_request_response(error)

    @swagger_auto_schema(
        tags=['Возможные значения поля заявки'],
        operation_description="Удаление возможного значения поля",
        responses={
            '400': 'Ошибка при удалении возможного значения поля: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Возможное значение успешно удалено'
        }
    )
    def delete(self, request, *args, **kwargs):
        try:
            name = FieldAvailableValuesUtils.delete_available_value_by_object_id(self.kwargs['value_id'])
            self.journal.write(
                self.pu.get_display_name('django_user_id', request.user.id),
                SUCCESS,
                f'Удалено возможное значения поля: {name}'
            )
            return self.ru.ok_response('Возможное значение успешно удалено')
        except Exception:
            error = ExceptionHandling.get_traceback()
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при удалении возможного значения поля: {error}'
            )
            return self.ru.bad_request_response(error)
