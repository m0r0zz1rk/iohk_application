from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.applications.serializers.app_fields_serializer import AppFieldsSerializer, AppFieldSaveSerializer
from apps.applications.utils.app_fields import AppFieldsUtils
from apps.commons.consts.journals.journal_event_results import SUCCESS, ERROR
from apps.commons.consts.journals.journal_rec_types import ADMINS
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


class EventAppFieldsViewSet(viewsets.ModelViewSet):
    """API для работы полями формы заявки на мероприятие"""
    permission_classes = [IsAuth, IsAdministrators]
    serializer_class = AppFieldsSerializer

    journal = JournalWriter(ADMINS)
    ru = ResponseUtils()
    restu = RestUtils()
    du = DictUtils()
    dateu = DateUtils()
    pu = ProfileUtils()
    eu = EventsUtils()

    @swagger_auto_schema(
        tags=['Поля формы заявки  (ЛК Администратора)'],
        operation_description="Получение списка полей формы заявки",
        responses={
            '400': 'Ошибка при получении списка: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': AppFieldsSerializer(many=True),
        }
    )
    def list(self, request, *args, **kwargs):
        """Получение списка полей формы заявки"""
        try:
            queryset = AppFieldsUtils.get_app_fields_for_event(
                self.kwargs['event_id'],
                self.kwargs['app_type']
            )
            serializer = self.get_serializer(queryset, many=True)
            self.journal.write(
                self.pu.get_display_name('django_user_id', request.user.id),
                SUCCESS,
                'Получение списка полей формы заявки'
            )
            return self.ru.ok_response_dict(serializer.data)
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при получении списка полей формы заявки: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при получении списка полей формы заявки'
            )

    @swagger_auto_schema(
        tags=['Поля формы заявки  (ЛК Администратора)'],
        request_body=AppFieldSaveSerializer,
        operation_description="Добавление поля формы заявки",
        responses={
            '400': 'Ошибка при добавлении поля: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Поле успешно добавлено'
        }
    )
    def save(self, request, *args, **kwargs):
        """Добавление поля формы заявки"""
        serialize = AppFieldSaveSerializer(data=request.data)
        if serialize.is_valid(raise_exception=True):
            serialize.save()
            self.journal.write(
                self.pu.get_display_name('django_user_id', request.user.id),
                SUCCESS,
                f'Добавлено новое поле формы заявки "'
                f'{self.du.get_str_value_in_dict_by_key(
                    'name',
                    request.data
                )} " для мероприятия "{
                    self.eu.get_event_by_object_id(serialize.data['event']).name
                }"'
            )
            return self.ru.ok_response('Поле успешно добавлено')
        else:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при добавлении поля формы заявки: {serialize.errors}'
            )
            return self.ru.bad_request_response(serialize.errors)

    @swagger_auto_schema(
        tags=['Поля формы заявки  (ЛК Администратора)'],
        request_body=AppFieldSaveSerializer,
        operation_description="Изменение поля формы заявки",
        responses={
            '400': 'Ошибка при изменении поля формы заявки: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Поле успешно изменено'
        }
    )
    def edit(self, request, *args, **kwargs):
        """Изменение поля формы заявки"""
        field = AppFieldsUtils.get_app_field_by_object_id(self.kwargs['field_id'])
        serialize = AppFieldSaveSerializer(
            field,
            data=request.data,
            partial=True
        )
        if serialize.is_valid(raise_exception=True):
            serialize.save()
            self.journal.write(
                self.pu.get_display_name('django_user_id', request.user.id),
                SUCCESS,
                f'Изменено поле формы заявки "'
                f'{self.du.get_str_value_in_dict_by_key(
                    'name',
                    request.data
                )} " для мероприятия "{
                    self.eu.get_event_by_object_id(serialize.data['event']).name
                }"'
            )
            return self.ru.ok_response('Поле успешно изменено')
        else:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при изменении поля: {serialize.errors}'
            )
            return self.ru.bad_request_response(serialize.errors)

    @swagger_auto_schema(
        tags=['Поля формы заявки  (ЛК Администратора)'],
        operation_description="Удаление поля формы заявки",
        responses={
            '400': 'Ошибка при удалении поля: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Поле успешно удалено'
        }
    )
    def delete(self, request, *args, **kwargs):
        try:
            name = AppFieldsUtils.delete_app_field_by_object_id(self.kwargs['field_id'])
            if name is not None:
                self.journal.write(
                    self.pu.get_display_name('django_user_id', request.user.id),
                    SUCCESS,
                    f'Удалено мероприятие: {name}'
                )
                return self.ru.ok_response('Мероприятие успешно удалено')
            else:
                return self.ru.sorry_try_again_response()
        except Exception:
            error = ExceptionHandling.get_traceback()
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при удалении мероприятия: {error}'
            )
            return self.ru.bad_request_response(error)
