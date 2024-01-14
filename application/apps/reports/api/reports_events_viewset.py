from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.commons.consts.journals.journal_event_results import ERROR
from apps.commons.consts.journals.journal_rec_types import REPORTS
from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.permissions.is_auth import IsAuth
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.events.filters.events_filter import EventsFilter
from apps.events.serializers.events_serializer import EventsShortSerializer
from apps.events.utils.events import EventsUtils
from apps.journals.writer.journal_writer import JournalWriter


class ReportsEventsViewSet(viewsets.ModelViewSet):
    """API для работы с мероприятиями для формирования отчетов"""
    permission_classes = [IsAuth, IsAdministrators]
    queryset = EventsUtils.get_all_events()
    serializer_class = EventsShortSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend,]
    filterset_class = EventsFilter

    journal = JournalWriter(REPORTS)
    ru = ResponseUtils()
    eu = EventsUtils()

    @swagger_auto_schema(
        tags=['Отчеты'],
        operation_description="Получение списка мероприятий (краткая информация)",
        responses={
            '400': 'Ошибка при получении списка мероприятий: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': EventsShortSerializer(many=True),
        }
    )
    def list(self, request, *args, **kwargs):
        """Получение мероприятий"""
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return self.ru.ok_response_dict(serializer.data)
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при получении списка мероприятий для формирования отчета: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при получении мероприятий'
            )
