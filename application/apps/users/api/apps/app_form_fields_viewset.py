from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.applications.serializers.app_fields_serializer import ShortAppFieldSerializer
from apps.applications.serializers.app_form_fields_serializer import AppFormFieldSaveSerializer, \
    PartAppFormRecSaveSerializer, PartAppFormRecSerializer, PartAppFormRecDeleteSerializer
from apps.applications.utils.app_fields import AppFieldsUtils
from apps.applications.utils.app_form_fields import AppFormFieldsUtils
from apps.authen.utils.profile import ProfileUtils
from apps.commons.consts.journals.journal_event_results import ERROR, SUCCESS
from apps.commons.consts.journals.journal_rec_types import APPLICATIONS
from apps.commons.permissions.is_users import IsUsers
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.journals.writer.journal_writer import JournalWriter


class AppFormFieldsViewSet(viewsets.ViewSet):
    """API для работы с полями заявок"""
    permission_classes = [IsAuthenticated, IsUsers]
    journal = JournalWriter(APPLICATIONS)
    ru = ResponseUtils()
    pu = ProfileUtils()

    @swagger_auto_schema(
        tags=['Поля заявок (ЛК пользователя)'],
        request_body=AppFormFieldSaveSerializer,
        operation_description="Сохранение значения поля",
        responses={
            '400': 'Ошибка при сохранении. Повторите попытку позже',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '204': 'Заявка не обнаружена',
            '200': 'Значение сохранено'
        }
    )
    def save_field_value(self, request, *args, **kwargs):
        """Сохранение значения поля"""
        try:
            serialize = AppFormFieldSaveSerializer(data=request.data)
            if serialize.is_valid(raise_exception=True):
                AppFormFieldsUtils.save_field_value(
                    serialize.data['field_id'],
                    serialize.data['value']
                )
                self.journal.write(
                    self.pu.get_display_name('django_user_id', request.user.id),
                    SUCCESS,
                    f'Значение "{AppFormFieldsUtils.get_dunder_str_field(serialize.data['field_id'])}" '
                    f'успешно сохранено'
                )
                return self.ru.ok_response_no_data()
            else:
                self.journal.write(
                    'Система',
                    ERROR,
                    f'Запрос на сохранения значения заполненного поля заявки не прошел сериализацию'
                )
                return self.ru.sorry_try_again_response()
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при сохранении значения заполненного поля заявки: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при сохранении значения заполненного поля заявки. Повторите попытку позже'
            )

    @swagger_auto_schema(
        tags=['Поля заявок (ЛК пользователя)'],
        operation_description="Получение списка полей формы заявок участников от пользователя",
        responses={
            '400': 'Ошибка при получении списка. Повторите попытку позже',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': ShortAppFieldSerializer(many=True)
        }
    )
    def get_part_app_fields(self, request, *args, **kwargs):
        """Получение списка полей формы заявки участников от пользователя"""
        try:
            form_fields = AppFieldsUtils.get_app_fields_for_event(
                self.kwargs['event_id'],
                'part_app'
            )
            if form_fields is not None:
                serialize = ShortAppFieldSerializer(form_fields, many=True)
                return self.ru.ok_response(serialize.data)
            else:
                self.journal.write(
                    'Система',
                    ERROR,
                    f'Ошибка при получении полей заявки участников от пользователя'
                )
                return self.ru.sorry_try_again_response()
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при получении списка: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при получении списка. Повторите попытку позже'
            )

    @swagger_auto_schema(
        tags=['Поля заявок (ЛК пользователя)'],
        operation_description="Получение списка записей заполненных полей заявок участников от пользователя",
        responses={
            '400': 'Ошибка при получении списка. Повторите попытку позже',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': PartAppFormRecSerializer(many=True)
        }
    )
    def get_part_app_recs(self, request, *args, **kwargs):
        """Получение списка записей заполненных полей заявок участников от пользователя"""
        try:
            profile = ProfileUtils.get_profile_by_user_id(request.user.id)
            recs = AppFormFieldsUtils.get_part_form_recs_for_app(
                profile.object_id,
                self.kwargs['event_id']
            )
            if recs is None:
                return self.ru.bad_request_no_data()
            serialize = PartAppFormRecSerializer(data=recs, many=True)
            if serialize.is_valid(raise_exception=True):
                return self.ru.ok_response_dict(serialize.data)
            else:
                self.journal.write(
                    'Система',
                    ERROR,
                    f'Ошибка сериализации при получении записей '
                    f'заполненных полей заявок участников от пользователя'
                )
                return self.ru.sorry_try_again_response()
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при получении списка: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при получении списка. Повторите попытку позже'
            )

    @swagger_auto_schema(
        tags=['Поля заявок (ЛК пользователя)'],
        request_body=PartAppFormRecSaveSerializer,
        operation_description="Сохранение заявки участника от пользователя",
        responses={
            '400': 'Ошибка при сохранении заявки. Повторите попытку позже',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Заявка успешно сохранена'
        }
    )
    def save_part_app_rec(self, request, *args, **kwargs):
        """Сохранение заявки участника от пользователя"""
        try:
            serialize = PartAppFormRecSaveSerializer(data=request.data)
            if serialize.is_valid(raise_exception=True):
                profile = ProfileUtils.get_profile_by_user_id(request.user.id)
                process = AppFormFieldsUtils.save_part_app_rec(
                    profile.object_id,
                    self.kwargs['event_id'],
                    serialize.data['rec_id'],
                    serialize.data['fields']
                )
                if process:
                    return self.ru.ok_response('Заявка успешно сохранена')
                else:
                    self.journal.write(
                        'Система',
                        ERROR,
                        f'Ошибка при сохранении заявки участника от пользователя: '
                        f'функция save_part_app_rec'
                    )
                    return self.ru.sorry_try_again_response()
            else:
                self.journal.write(
                    'Система',
                    ERROR,
                    f'Ошибка при сохранении заявки участника от пользователя: '
                    f'полученные данные не прошли сериализацию'
                )
                return self.ru.bad_request_response('Полученные данные не прошли сериализацию')
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при сохранении заявки участника от пользователя: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при сохранении заявки. Повторите попытку позже'
            )

    @swagger_auto_schema(
        tags=['Поля заявок (ЛК пользователя)'],
        request_body=PartAppFormRecSaveSerializer,
        operation_description="Изменение заявки участника от пользователя",
        responses={
            '400': 'Ошибка при изменении заявки. Повторите попытку позже',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Заявка успешно изменена'
        }
    )
    def edit_part_app_rec(self, request, *args, **kwargs):
        """Изменение заявки участника от пользователя"""
        try:
            serialize = PartAppFormRecSaveSerializer(data=request.data)
            if serialize.is_valid(raise_exception=True):
                profile = ProfileUtils.get_profile_by_user_id(request.user.id)
                process = AppFormFieldsUtils.edit_part_app_rec(
                    profile.object_id,
                    self.kwargs['event_id'],
                    serialize.data['rec_id'],
                    serialize.data['fields']
                )
                if process:
                    return self.ru.ok_response('Заявка успешно изменена')
                else:
                    self.journal.write(
                        'Система',
                        ERROR,
                        f'Ошибка при изменении заявки участника от пользователя: '
                        f'функция save_part_app_rec'
                    )
                    return self.ru.sorry_try_again_response()
            else:
                self.journal.write(
                    'Система',
                    ERROR,
                    f'Ошибка при изменении заявки участника от пользователя: '
                    f'полученные данные не прошли сериализацию'
                )
                return self.ru.bad_request_response('Полученные данные не прошли сериализацию')
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при изменении заявки участника от пользователя: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при изменении заявки. Повторите попытку позже'
            )

    @swagger_auto_schema(
        tags=['Поля заявок (ЛК пользователя)'],
        request_body=PartAppFormRecDeleteSerializer,
        operation_description="Удаление заявки участника от пользователя",
        responses={
            '400': 'Ошибка при удалении заявки. Повторите попытку позже',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Заявка успешно удалена'
        }
    )
    def delete_part_app_rec(self, request, *args, **kwargs):
        """Удаление заявки участника от пользователя"""
        try:
            serialize = PartAppFormRecDeleteSerializer(data=request.data)
            if serialize.is_valid(raise_exception=True):
                profile = ProfileUtils.get_profile_by_user_id(request.user.id)
                process = AppFormFieldsUtils.del_part_app_rec(
                    profile.object_id,
                    serialize.data['event_id'],
                    serialize.data['rec_id']
                )
                if process:
                    return self.ru.ok_response('Заявка успешно удалена')
                else:
                    self.journal.write(
                        'Система',
                        ERROR,
                        f'Ошибка при удалении заявки участника от пользователя: '
                        f'функция save_part_app_rec'
                    )
                    return self.ru.sorry_try_again_response()
            else:
                self.journal.write(
                    'Система',
                    ERROR,
                    f'Ошибка при удалении заявки участника от пользователя: '
                    f'полученные данные не прошли сериализацию'
                )
                return self.ru.bad_request_response('Полученные данные не прошли сериализацию')
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при удалении заявки участника от пользователя: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при удалении заявки. Повторите попытку позже'
            )
