from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.applications.utils.app_form_fields import AppFormFieldsUtils
from apps.applications.utils.apps import AppsUtils
from apps.authen.utils.profile import ProfileUtils
from apps.commons.consts.apps.app_statuses import CREATED
from apps.commons.consts.journals.journal_event_results import ERROR, SUCCESS
from apps.commons.consts.journals.journal_rec_types import APPLICATIONS
from apps.commons.permissions.is_users import IsUsers
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.journals.writer.journal_writer import JournalWriter
from apps.users.serializers.apps.app_info_serializer import AppInfoSerializer
from apps.users.serializers.apps.app_serializer import AppSaveSerializer
from apps.users.serializers.apps.app_user_serializer import AppUserSerializer


class AppsViewSet(viewsets.ViewSet):
    """API для работы с заявками пользователя"""
    permission_classes = [IsAuthenticated, IsUsers]
    journal = JournalWriter(APPLICATIONS)
    ru = ResponseUtils()
    pu = ProfileUtils()

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
            profile = self.pu.get_profile_by_user_id(request.user.id)
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
        operation_description="Подача заявки на участие в мероприятии",
        responses={
            '400': 'Ошибка при проверке подачи заявки. Повторите попытку позже',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Заявка успешно подана'
        }
    )
    def app_submit(self, request, *args, **kwargs):
        try:
            profile = self.pu.get_profile_by_user_id(request.user.id)
            process = AppsUtils.app_submit(
                profile.object_id,
                self.kwargs['event_id']
            )
            if process:
                return self.ru.ok_response('Заявка успешно подана')
            else:
                self.journal.write(
                    'Система',
                    ERROR,
                    f'Ошибка при подачи заявки: '
                    f'ошибка в функции app_submit'
                )
                return self.ru.bad_request_response(
                    f'Ошибка при подачи заявки. Повторите попытку позже'
                )
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при подачи заявки: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при подачи заявки. Повторите попытку позже'
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
            profile = self.pu.get_profile_by_user_id(request.user.id)
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
        operation_description="Получение списка заполненных полей заявки",
        responses={
            '400': 'Ошибка при получении списка. Повторите попытку позже',
            '401': 'Пользователь не авторизован',
            '200': AppUserSerializer(many=True)
        }
    )
    def get_app_fields(self, request, *args, **kwargs):
        """Получение списка заполненных полей заявки"""
        try:
            profile = self.pu.get_profile_by_user_id(request.user.id)
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
                f'Ошибка при получении списка. Повторите попытку позже'
            )

    @swagger_auto_schema(
        tags=['Заявки (ЛК пользователя)'],
        request_body=AppSaveSerializer,
        operation_description="Сохранение заявки",
        responses={
            '400': 'Ошибка при сохранении. Повторите попытку позже',
            '401': 'Пользователь не авторизован',
            '204': 'Заявка не обнаружена',
            '200': 'Заявка успешно сохранена'
        }
    )
    def save_app(self, request, *args, **kwargs):
        """Сохранение заявки"""
        try:
            serialize = AppSaveSerializer(data=request.data)
            if serialize.is_valid(raise_exception=True):
                for field in serialize.data['fields']:
                    field_id = value = ''
                    for k,v in field.items():
                        if k == 'field_id':
                            field_id = v
                        if k == 'value':
                            value = v
                    AppFormFieldsUtils.save_field_value(
                        field_id,
                        value
                    )
                app = AppsUtils.get_app_by_user_and_event_id(request.user.id, serialize.data['event_id'])
                AppsUtils.change_app_status(
                    app.object_id,
                    CREATED
                )
                self.journal.write(
                    self.pu.get_display_name('django_user_id', request.user.id),
                    SUCCESS,
                    f'У заявки изменен статус на "Сохранена"'
                )
                return self.ru.ok_response_no_data()
            else:
                self.journal.write(
                    'Система',
                    ERROR,
                    f'Запрос на сохранение заявки не прошел сериализацию'
                )
                return self.ru.sorry_try_again_response()
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при сохранении заявки: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при сохранении заявки. Повторите попытку позже'
            )

