from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.commons.permissions.is_users import IsUsers
from apps.admins.serializers.guides.events_types_serializer import EventsTypeSerializer
from apps.commons.consts.journals.journal_event_results import ERROR
from apps.commons.consts.journals.journal_rec_types import USERS
from apps.commons.permissions.is_auth import IsAuth
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.events.utils.events_type import EventsTypesUtils
from apps.journals.writer.journal_writer import JournalWriter


class EventsTypesViewSet(viewsets.ModelViewSet):
    """API для получения типов мероприятий"""
    permission_classes = [IsAuth, IsUsers]
    queryset = EventsTypesUtils.get_events_type()
    serializer_class = EventsTypeSerializer

    journal = JournalWriter(USERS)
    ru = ResponseUtils()

    @swagger_auto_schema(
        tags=['Типы мероприятий (ЛК пользователя)'],
        operation_description="Получение типов мероприятий",
        responses={
            '400': 'Ошибка при получении списка типов мероприятий: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': EventsTypeSerializer(many=True),
        }
    )
    def list(self, request, *args, **kwargs):
        """Получение типов мероприятий"""
        try:
            serializer = self.get_serializer(self.get_queryset(), many=True)
            return self.ru.ok_response_dict(serializer.data)
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при получении типов мероприятий: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при получении типов мероприятий'
            )
