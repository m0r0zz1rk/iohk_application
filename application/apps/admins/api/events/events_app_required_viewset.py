from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.events.serializers.events_apps_required_serializer import EventsAppsRequiredSerializer, \
    EventsAppsRequiredChangeSerializer
from apps.commons.consts.journals.journal_event_results import SUCCESS, ERROR
from apps.commons.consts.journals.journal_rec_types import ADMINS
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.permissions.is_auth import IsAuth
from apps.commons.utils.data_types.date import DateUtils
from apps.commons.utils.data_types.dict import DictUtils
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.commons.utils.django.rest import RestUtils
from apps.events.utils.events import EventsUtils
from apps.events.utils.events_app_required import EventsAppsRequiredUtils
from apps.authen.utils.profile import ProfileUtils
from apps.journals.writer.journal_writer import JournalWriter


class EventsAppRequiredViewSet(viewsets.ModelViewSet):
    """API для работы с записями необходимости заявок для мероприятий"""
    permission_classes = [IsAuth, IsAdministrators]
    queryset = EventsAppsRequiredUtils.get_all_apps_required()
    serializer_class = EventsAppsRequiredSerializer

    journal = JournalWriter(ADMINS)
    ru = ResponseUtils()
    restu = RestUtils()
    du = DictUtils()
    dateu = DateUtils()
    pu = ProfileUtils()
    eu = EventsUtils()

    @swagger_auto_schema(
        tags=['Необходимость форм заявок (ЛК Администратора)'],
        operation_description="Получение записи о необходимости форм заявок на мероприятие",
        responses={
            '400': 'Ошибка при получении записи: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': EventsAppsRequiredSerializer,
        }
    )
    def list(self, request, *args, **kwargs):
        """Получение записи о необходимости форм заявок на мероприятие"""
        try:
            queryset = EventsAppsRequiredUtils.get_apps_required_for_event(self.kwargs['event_id'])
            serializer = self.get_serializer(queryset)
            self.journal.write(
                self.pu.get_display_name('django_user_id', request.user.id),
                SUCCESS,
                f'Просмотр записи о необходимости форм заявок на мероприятие"'
                f'{EventsUtils.get_event_by_object_id(self.kwargs['event_id']).name}'
                f'"'
            )
            return self.ru.ok_response_dict(serializer.data)
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при получении записи о необходимости форм заявок на мероприятие: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при получении записи о необходимости форм заявок на мероприятие'
            )

    @swagger_auto_schema(
        tags=['Необходимость форм заявок (ЛК Администратора)'],
        request_body=EventsAppsRequiredChangeSerializer,
        operation_description="Изменение необходимости формы заявки",
        responses={
            '400': 'Ошибка при изменении необходимости формы заявки: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Изменение принято'
        }
    )
    def edit(self, request, *args, **kwargs):
        """Изменение необходимости формы заявки"""
        serialize = EventsAppsRequiredChangeSerializer(data=request.data)
        if serialize.is_valid(raise_exception=True):
            if EventsAppsRequiredUtils.change_app_required_for_event(serialize.data):
                self.journal.write(
                    self.pu.get_display_name('django_user_id', request.user.id),
                    SUCCESS,
                    f'Изменена необходимость форм заявок для мероприятия "'
                    f'{EventsUtils.get_event_by_object_id(serialize.data['event_id']).name}'
                    f'"'
                )
                return self.ru.ok_response_dict('Изменение принято')
        self.journal.write(
            'Система',
            ERROR,
            f'Ошибка при изменении необходимости формы заявки: {serialize.errors}'
        )
        return self.ru.bad_request_response(serialize.errors)
