from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.events.filters.events_information_filter import EventsInformationFilter
from apps.events.serializers.events_information_serializer import EventsInformationSerializer, \
    EventsInformationSaveSerializer
from apps.commons.consts.journals.journal_event_results import SUCCESS, ERROR
from apps.commons.consts.journals.journal_rec_types import ADMINS
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.permissions.is_auth import IsAuth
from apps.commons.utils.data_types.dict import DictUtils
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.commons.utils.django.rest import RestUtils
from apps.events.utils.events import EventsUtils
from apps.events.utils.events_information import EventsInformationUtils
from apps.authen.utils.profile import ProfileUtils
from apps.journals.writer.journal_writer import JournalWriter


class EventsInformationViewSet(viewsets.ModelViewSet):
    """API для работы с информационными сообщениями о мероприятиях"""
    permission_classes = [IsAuth, IsAdministrators]
    queryset = EventsInformationUtils.get_all_information()
    serializer_class = EventsInformationSerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_class = EventsInformationFilter

    journal = JournalWriter(ADMINS)
    ru = ResponseUtils()
    restu = RestUtils()
    du = DictUtils()
    pu = ProfileUtils()
    eu = EventsUtils()

    @swagger_auto_schema(
        tags=['Информационные сообщения (ЛК Администратора)'],
        operation_description="Получение информационного сообщения о мероприятии",
        responses={
            '400': 'Ошибка при получении информационного сообщения: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': EventsInformationSerializer,
        }
    )
    def list(self, request, *args, **kwargs):
        """Получение информационного сообщения о мероприятии"""
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            self.journal.write(
                self.pu.get_display_name('django_user_id', request.user.id),
                SUCCESS,
                'Просмотр информационного сообщения'
            )
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

    @swagger_auto_schema(
        tags=['Информационные сообщения (ЛК Администратора)'],
        request_body=EventsInformationSaveSerializer,
        operation_description="Сохранение информационного сообщения",
        responses={
            '400': 'Ошибка при сохранении информационного сообщения: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Информация успешно сохранена'
        }
    )
    def save(self, request, *args, **kwargs):
        """Сохранение информационного сообщения"""
        try:
            information = EventsInformationUtils.get_event_information_by_event_id(self.kwargs['event_id'])
            serialize = self.serializer_class(information, data=request.data, partial=True)
            if serialize.is_valid(raise_exception=True):
                serialize.save()
                self.journal.write(
                    self.pu.get_display_name('django_user_id', request.user.id),
                    SUCCESS,
                    f'Информационное сообщение для "{information.event.name}" успешно сохранено')
                return self.ru.ok_response('Информация успешно сохранена')
            else:
                self.journal.write(
                    'Система',
                    ERROR,
                    f'Ошибка при сохранении информационного сообщения: {serialize.errors}'
                )
                return self.ru.bad_request_response(serialize.errors)
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при сохранении информационного сообщения: {ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response('Ошибка при сохранении информационного сообщения')
