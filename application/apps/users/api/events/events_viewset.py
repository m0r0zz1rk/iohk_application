from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.commons.consts.journals.journal_event_results import ERROR
from apps.commons.consts.journals.journal_rec_types import USERS
from apps.commons.permissions.is_auth import IsAuth
from apps.commons.permissions.is_users import IsUsers
from apps.commons.utils.data_types.date import DateUtils
from apps.commons.utils.data_types.dict import DictUtils
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.commons.utils.django.rest import RestUtils
from apps.events.utils.events import EventsUtils
from apps.authen.utils.profile import ProfileUtils
from apps.journals.writer.journal_writer import JournalWriter
from apps.users.serializers.events_serializer import EventsShortInfoSerializer


class EventsViewSet(viewsets.ModelViewSet):
    """API для работы с мероприятиями в личном кабинете пользователя"""
    permission_classes = [IsAuth, IsUsers]
    queryset = EventsUtils.get_all_events()
    serializer_class = EventsShortInfoSerializer

    journal = JournalWriter(USERS)
    ru = ResponseUtils()
    restu = RestUtils()
    du = DictUtils()
    dateu = DateUtils()
    pu = ProfileUtils()
    eu = EventsUtils()

    @swagger_auto_schema(
        tags=['Мероприятия (ЛК пользователя)'],
        manual_parameters=[
            openapi.Parameter(
                'event_type',
                openapi.IN_QUERY,
                description="Тип мероприятия",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],
        operation_description="Получение мероприятий определенного типа",
        responses={
            '400': 'Ошибка при получении списка мероприятий: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': EventsShortInfoSerializer(many=True),
        }
    )
    def list(self, request, *args, **kwargs):
        """Получение мероприятий определенного типа"""
        try:
            queryset = EventsUtils.get_events_by_event_type_and_group(
                request.GET['event_type'],
                request.user.groups.first().name
            )
            serializer = self.get_serializer(queryset, many=True)
            return self.ru.ok_response_dict(serializer.data)
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при получении списка мероприятий: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при получении списка мероприятий'
            )
