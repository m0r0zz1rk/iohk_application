from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.applications.utils.apps import AppsUtils
from apps.authen.utils.profile import ProfileUtils
from apps.commons.consts.journals.journal_event_results import SUCCESS, ERROR
from apps.commons.consts.journals.journal_rec_types import APPLICATIONS
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.journals.writer.journal_writer import JournalWriter
from apps.users.serializers.apps.app_serializer import AppChangeStatusSerializer


class AppStatusViewSet(viewsets.ViewSet):
    """API для работы со статусами заявок"""
    permission_classes = [IsAuthenticated, ]
    journal = JournalWriter(APPLICATIONS)
    ru = ResponseUtils()
    pu = ProfileUtils()

    @swagger_auto_schema(
        tags=['Заявки (ЛК пользователя/администратора)'],
        request_body=AppChangeStatusSerializer,
        operation_description="Изменение статуса заявки",
        responses={
            '400': 'Ошибка при изменении. Повторите попытку позже',
            '401': 'Пользователь не авторизован',
            '204': 'Заявка не обнаружена',
            '200': 'Статус заявки успешно изменен'
        }
    )
    def app_status_change(self, request, *args, **kwargs):
        """Изменение статуса заявки"""
        try:
            serialize = AppChangeStatusSerializer(data=request.data)
            if serialize.is_valid(raise_exception=True):
                app = AppsUtils.get_app_by_user_and_event_id(
                    request.user.id,
                    serialize.data['entity_id']
                )
                if app is None:
                    app = AppsUtils.get_app_by_object_id(
                        serialize.data['entity_id']
                    )
                AppsUtils.change_app_status(
                    app.object_id,
                    serialize.data['status'],
                    serialize.data['message']
                )
                self.journal.write(
                    self.pu.get_display_name('django_user_id', request.user.id),
                    SUCCESS,
                    f'Статус заявки "{app}" успешно изменен'
                )
                return self.ru.ok_response_no_data()
            else:
                self.journal.write(
                    'Система',
                    ERROR,
                    f'Запрос на изменение статуса не прошел сериализацию'
                )
                return self.ru.sorry_try_again_response()
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при изменении статуса заявки: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при изменении статуса заявки. Повторите попытку позже'
            )