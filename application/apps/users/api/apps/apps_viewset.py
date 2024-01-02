from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.applications.utils.app_form_fields import AppFormFieldsUtils
from apps.applications.utils.apps import AppsUtils
from apps.authen.utils.profile import ProfileUtils
from apps.commons.consts.journals.journal_event_results import ERROR
from apps.commons.consts.journals.journal_rec_types import APPLICATIONS
from apps.commons.permissions.is_users import IsUsers
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.journals.writer.journal_writer import JournalWriter
from apps.users.serializers.app_info_serializer import AppInfoSerializer
from apps.users.serializers.app_user_serializer import AppUserSerializer


class AppsViewSet(viewsets.ViewSet):
    """API для работы с заявками пользователя"""
    permission_classes = [IsAuthenticated, IsUsers]
    journal = JournalWriter(APPLICATIONS)
    ru = ResponseUtils()

    @swagger_auto_schema(
        tags=['Заявки (ЛК пользователя)'],
        operation_description="Проверка на наличие заявки на участие в мероприятии",
        responses={
            '400': 'Ошибка при проверке наличия заявки. Повторите попытку позже',
            '401': 'Пользователь не авторизован',
            '204': 'Заявка не обнаружена',
            '200': 'Заявка обнаружена'
        }
    )
    def check_app_exist(self, request, *args, **kwargs):
        """Проверка на наличие заявки"""
        try:
            profile = ProfileUtils.get_profile_by_user_id(request.user.id)
            check = AppsUtils.check_event_app_for_user(profile.object_id, self.kwargs['event_id'])
            if check:
                return self.ru.ok_response_no_data()
            else:
                return self.ru.no_content_response()
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при проверке наличия заявки: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при проверке наличия заявки. Повторите попытку позже'
            )

    @swagger_auto_schema(
        tags=['Заявки (ЛК пользователя)'],
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
            profile = ProfileUtils.get_profile_by_user_id(request.user.id)
            app = AppsUtils.get_app_by_profile_and_event_id(
                profile.object_id,
                self.kwargs['event_id']
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
        tags=['Заявки (ЛК пользователя)'],
        operation_description="Получение списка заполненных полей заявки пользователя",
        responses={
            '400': 'Ошибка при получении списка. Повторите попытку позже',
            '401': 'Пользователь не авторизован',
            '200': AppUserSerializer(many=True)
        }
    )
    def get_user_app_fields(self, request, *args, **kwargs):
        """Получение списка заполненных полей заявки пользователя"""
        try:
            profile = ProfileUtils.get_profile_by_user_id(request.user.id)
            form_fields = AppFormFieldsUtils.get_user_form_fields_for_app(
                profile.object_id,
                self.kwargs['event_id']
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
                f'Ошибка при получении списка: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'ООшибка при получении списка. Повторите попытку позже'
            )