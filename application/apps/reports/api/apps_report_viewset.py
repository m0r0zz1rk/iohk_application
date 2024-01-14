from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.commons.consts.journals.journal_event_results import ERROR
from apps.commons.consts.journals.journal_rec_types import REPORTS
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.permissions.is_auth import IsAuth
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.events.utils.events import EventsUtils
from apps.journals.writer.journal_writer import JournalWriter
from apps.reports.excel_factory import ExcelFactory
from apps.reports.serializers.apps_report_serializer import AppsReportSerializer
from apps.reports.utils.apps_report import AppsReportUtils


class AppsReportViewSet(viewsets.ViewSet):
    """API для работы с отчетом, содержащим заявки на мероприятие"""
    permission_classes = [IsAuth, IsAdministrators]

    journal = JournalWriter(REPORTS)
    ru = ResponseUtils()
    eu = EventsUtils()
    ef = ExcelFactory()

    @swagger_auto_schema(
        tags=['Отчеты'],
        operation_description="Получение Excel-файла с заявками на мероприятие",
        request_body=AppsReportSerializer,
        responses={
            '400': 'Ошибка при получении файла: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Excel файл с заявками на мероприятие',
        }
    )
    def apps_report(self, request, *args, **kwargs):
        try:
            serialize = AppsReportSerializer(data=request.data)
            if serialize.is_valid(raise_exception=True):
                aru = AppsReportUtils(
                    event_id=request.data['event_id'],
                    apps_types=request.data['apps_types']
                )
                event = EventsUtils.get_event_by_object_id(request.data['event_id'])
                content = aru.content_data()
                return self.ef.download_excel(
                    f'{event.name}.xlsx',
                    content
                )
            else:
                self.journal.write(
                    'Система',
                    ERROR,
                    f'Ошибка сериализации при получении Excel файла с заявками '
                    f'на мероприятие'
                )
                return self.ru.bad_request_response(
                    f'Ошибка сериализации данных. Повторите попытку позже'
                )
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при получении Excel файла с заявками: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при получении Excel файла с заявками. Повторите попытку позже'
            )
