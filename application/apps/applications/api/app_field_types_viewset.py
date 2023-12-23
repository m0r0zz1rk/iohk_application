from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.applications.serializers.app_field_types_serializer import AppFieldTypesSerializer
from apps.applications.utils.app_field_types import AppFieldTypesUtils
from apps.commons.consts.journals.journal_event_results import SUCCESS, ERROR
from apps.commons.consts.journals.journal_rec_types import APPLICATIONS
from apps.commons.permissions.is_auth import IsAuth
from apps.commons.utils.data_types.date import DateUtils
from apps.commons.utils.data_types.dict import DictUtils
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.commons.utils.django.rest import RestUtils
from apps.events.utils.events import EventsUtils
from apps.authen.utils.profile import ProfileUtils
from apps.journals.writer.journal_writer import JournalWriter


class AppFieldTypesViewSet(viewsets.ModelViewSet):
    """API для работы с типами полей форм заявок"""
    permission_classes = [IsAuth]
    queryset = AppFieldTypesUtils.get_all_types()
    serializer_class = AppFieldTypesSerializer

    journal = JournalWriter(APPLICATIONS)
    ru = ResponseUtils()
    restu = RestUtils()
    du = DictUtils()
    dateu = DateUtils()
    pu = ProfileUtils()
    eu = EventsUtils()

    @swagger_auto_schema(
        tags=['Типы полей заявок'],
        operation_description="Получение типов полей заявок",
        responses={
            '400': 'Ошибка при получении типов полей заявок: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '200': AppFieldTypesSerializer(many=True),
        }
    )
    def list(self, request, *args, **kwargs):
        """Получение типов полей заявок"""
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset)
            self.journal.write(
                self.pu.get_display_name('django_user_id', request.user.id),
                SUCCESS,
                f'Получение типов полей заявок'
            )
            return self.ru.ok_response_dict(serializer.data)
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при получении типов полей заявок: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при получении типов полей заявок'
            )
