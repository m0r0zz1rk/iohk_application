from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.applications.serializers.app_fields_serializer import ShortAppFieldSerializer
from apps.applications.serializers.app_form_fields_serializer import PartAppFormRecSerializer
from apps.applications.utils.app_fields import AppFieldsUtils
from apps.applications.utils.app_form_fields import AppFormFieldsUtils
from apps.applications.utils.apps import AppsUtils
from apps.authen.utils.profile import ProfileUtils
from apps.commons.consts.journals.journal_event_results import ERROR
from apps.commons.consts.journals.journal_rec_types import APPLICATIONS
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.journals.writer.journal_writer import JournalWriter
from apps.users.serializers.apps.app_info_serializer import AppInfoSerializer
from apps.users.serializers.apps.app_user_serializer import AppUserSerializer


class AdminAppsViewSet(viewsets.ViewSet):
    """API для работы с заявками пользователя в ЛК администратора"""
    permission_classes = [IsAuthenticated, IsAdministrators]
    journal = JournalWriter(APPLICATIONS)
    ru = ResponseUtils()
    pu = ProfileUtils()

    @swagger_auto_schema(
        tags=['Заявки (ЛК администратора)'],
        operation_description="Получение основной информации по заявке",
        responses={
            '400': 'Ошибка при получении информации. Повторите попытку позже',
            '401': 'Пользователь не авторизован',
            '200': AppInfoSerializer
        }
    )
    def get_app_info(self, request, *args, **kwargs):
        """Получение основной информации по заявке"""
        try:
            app = AppsUtils.get_app_by_object_id(
                self.kwargs['app_id']
            )
            serialize = AppInfoSerializer(app)
            return self.ru.ok_response_dict(serialize.data)
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при получении информации: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при получении информации. Повторите попытку позже'
            )

    @swagger_auto_schema(
        tags=['Заявки (ЛК администратора)'],
        operation_description="Получение списка заполненных полей заявки пользователя",
        responses={
            '400': 'Ошибка при получении списка. Повторите попытку позже',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': AppUserSerializer(many=True)
        }
    )
    def get_app_fields(self, request, *args, **kwargs):
        """Получение списка заполненных полей заявки пользователя"""
        try:
            form_fields = AppFormFieldsUtils.get_user_form_fields_for_app_by_app_id(
                self.kwargs['app_id']
            )
            if form_fields is not None:
                serialize = AppUserSerializer(form_fields, many=True)
                return self.ru.ok_response(serialize.data)
            else:
                self.journal.write(
                    'Система',
                    ERROR,
                    f'Ошибка при получении заполненных полей заявки пользователя'
                )
                return self.ru.sorry_try_again_response()
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при получении списка заполненных полей заявки пользователя: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при получении списка. Повторите попытку позже'
            )

    @swagger_auto_schema(
        tags=['Заявки (ЛК администратора)'],
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
            form_fields = AppFieldsUtils.get_app_fields_for_event_by_app_id(
                self.kwargs['app_id'],
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
                f'Ошибка при получении списка полей заявки участников от пользователя: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при получении списка полей заявки участников от пользователя. '
                f'Повторите попытку позже'
            )

    @swagger_auto_schema(
        tags=['Заявки (ЛК администратора)'],
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
            recs = AppFormFieldsUtils.get_part_form_recs_for_app_by_app_id(
                self.kwargs['app_id']
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
                f'Ошибка при получении списка '
                f'заполненных полей заявок участников от пользователя: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при получении списка заполненных полей заявок участников от пользователя'
                f'. Повторите попытку позже'
            )
