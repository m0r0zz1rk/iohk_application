from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.authen.utils.profile import ProfileUtils
from apps.commons.consts.journals.journal_event_results import ERROR
from apps.commons.consts.journals.journal_rec_types import EVENTS
from apps.commons.permissions.is_users import IsUsers
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.events.utils.events_app_required import EventsAppsRequiredUtils
from apps.journals.writer.journal_writer import JournalWriter
from apps.users.serializers.events_serializer import EventAppsRequiredSerializer


class EventAppRequiredViewSet(viewsets.ViewSet):
    """API для получения доступных форм заявок"""
    permission_classes = [IsAuthenticated, IsUsers]
    journal = JournalWriter(EVENTS)
    ru = ResponseUtils()
    pu = ProfileUtils()

    @swagger_auto_schema(
        tags=['Мероприятия (ЛК пользователя)'],
        operation_description="Получение типов форм заявок для мероприятия",
        responses={
            '400': 'Ошибка при получении информации. Повторите попытку позже',
            '401': 'Пользователь не авторизован',
            '200': EventAppsRequiredSerializer
        }
    )
    def get_app_required(self, request, *args, **kwargs):
        """Получение типов форм заявок для мероприятия"""
        try:
            app_required = EventsAppsRequiredUtils.get_apps_required_for_event(
                self.kwargs['event_id']
            )
            data = {
                'user_app': app_required.user_app_required,
                'part_app': app_required.participant_app_required
            }
            serialize = EventAppsRequiredSerializer(data)
            return self.ru.ok_response_dict(serialize.data)
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при получении типов форм заявок для мероприятия: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.sorry_try_again_response()
