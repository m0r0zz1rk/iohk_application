from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.commons.permissions.is_users import IsUsers
from apps.events.serializers.events_information_serializer import EventsInformationSerializer
from apps.commons.consts.journals.journal_event_results import ERROR
from apps.commons.consts.journals.journal_rec_types import ADMINS
from apps.commons.permissions.is_auth import IsAuth
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.events.utils.events_information import EventsInformationUtils
from apps.authen.utils.profile import ProfileUtils
from apps.journals.writer.journal_writer import JournalWriter


class EventInformationViewSet(viewsets.ModelViewSet):
    """API для получения информационного сообщения мероприятия"""
    permission_classes = [IsAuth, IsUsers]
    queryset = EventsInformationUtils.get_all_information()
    serializer_class = EventsInformationSerializer

    journal = JournalWriter(ADMINS)
    ru = ResponseUtils()
    pu = ProfileUtils()

    @swagger_auto_schema(
        tags=['Информационные сообщения (ЛК пользователя)'],
        operation_description="Получение информационного сообщения о мероприятии",
        responses={
            '400': 'Ошибка при получении списка мероприятий: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': EventsInformationSerializer,
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """Получение информационного сообщения о мероприятии"""
        try:
            info = EventsInformationUtils.get_event_information_by_event_id(self.kwargs['event_id'])
            serializer = self.get_serializer(info)
            return self.ru.ok_response_dict(serializer.data)
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при получении информационного сообщения о мероприятии: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при получении информационного сообщения о мероприятии'
            )
