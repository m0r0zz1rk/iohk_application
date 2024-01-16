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
from apps.reports.serializers.count_report_serializer import CountReportSerializer
from apps.reports.utils.count_report import CountReportUtils


class CountReportViewSet(viewsets.ViewSet):
    """API для работы с количественным отчетом"""
    permission_classes = [IsAuth, IsAdministrators]

    journal = JournalWriter(REPORTS)
    ru = ResponseUtils()
    eu = EventsUtils()
    ef = ExcelFactory()

    @swagger_auto_schema(
        tags=['Отчеты'],
        operation_description="Получение количественного отчета",
        request_body=CountReportSerializer,
        responses={
            '400': 'Ошибка при получении файла: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Excel файл количетсвенного отчета',
        }
    )
    def count_report(self, request, *args, **kwargs):
        try:
            serialize = CountReportSerializer(data=request.data)
            if serialize.is_valid(raise_exception=True):
                cru = CountReportUtils(
                    serialize.data['events'],
                    serialize.data['filters'],
                    serialize.data['apps_types'],
                    serialize.data['total_row']
                )
                content = cru.content_data()
                return self.ef.download_excel(
                    f'Количественный отчет.xlsx',
                    content
                )
            else:
                self.journal.write(
                    'Система',
                    ERROR,
                    f'Ошибка сериализации при получении количественного отчета'
                )
                return self.ru.bad_request_response(
                    f'Ошибка сериализации данных. Повторите попытку позже'
                )
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при получении количественного отчета: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при получении количественного отчета. Повторите попытку позже'
            )
