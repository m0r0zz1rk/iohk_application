from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.admins.serializers.main_serializer import AppsCountSerializer
from apps.commons.consts.journals.journal_event_results import ERROR
from apps.commons.consts.journals.journal_rec_types import ADMINS
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.events.utils.events import EventsUtils
from apps.journals.writer.journal_writer import JournalWriter


class MainViewSet(viewsets.ViewSet):
    """API для получения информация на главной странице ЛК администратора"""
    permission_classes = [IsAuthenticated, IsAdministrators]
    journal = JournalWriter(ADMINS)
    ru = ResponseUtils()

    @swagger_auto_schema(
        tags=['Главная страница (ЛК администратора)'],
        operation_description="Получение количества заявок по опубликованным мероприятиям",
        responses={
            '400': 'Ошибка при получении информации. Повторите попытку позже',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': AppsCountSerializer(many=True)
        }
    )
    def get_app_count_for_published_events(self, request, *args, **kwargs):
        """Получение количества заявок по опубликованным мероприятиям"""
        try:
            info = EventsUtils.get_apps_count_of_published_events()
            serialize = AppsCountSerializer(data=info, many=True)
            if serialize.is_valid(raise_exception=True):
                return self.ru.ok_response(serialize.data)
            else:
                self.journal.write(
                    'Система',
                    ERROR,
                    f'Ошибка сериализации при получении количества заявок по мероприятиям'
                )
                return self.ru.bad_request_response('Ошибка сериализации данных. Повторите попытку позже')
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при получении получении количества заявок по мероприятиям: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при получении получении количества заявок по мероприятиям. '
                f'Повторите попытку позже'
            )
