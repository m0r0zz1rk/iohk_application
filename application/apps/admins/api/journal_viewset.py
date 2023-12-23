from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.journals.filters.journal_filter import JournalFilter
from apps.journals.serializers.journal_serializer import JournalPaginationSerializer, JournalSerializer
from apps.commons.consts.journals.journal_event_results import SUCCESS, ERROR
from apps.commons.consts.journals.journal_rec_types import ADMINS
from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.permissions.is_auth import IsAuth
from apps.commons.utils.data_types.dict import DictUtils
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.commons.utils.django.rest import RestUtils
from apps.journals.utils.journal import JournalUtils
from apps.authen.utils.profile import ProfileUtils
from apps.journals.writer.journal_writer import JournalWriter


class JournalViewSet(viewsets.ModelViewSet):
    """API для работы с журналом"""
    permission_classes = [IsAuth, IsAdministrators]
    queryset = JournalUtils.get_all_records()
    serializer_class = JournalSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend,]
    filterset_class = JournalFilter

    journal = JournalWriter(ADMINS)
    ru = ResponseUtils()
    restu = RestUtils()
    du = DictUtils()
    pu = ProfileUtils()

    @swagger_auto_schema(
        tags=['Администрирование'],
        operation_description="Получение записей журнала",
        responses={
            '400': 'Ошибка при получении записей журнала: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': JournalPaginationSerializer,
        }
    )
    def list(self, request, *args, **kwargs):
        """Получение записей журнала"""
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            self.journal.write(
                self.pu.get_display_name('django_user_id', request.user.id),
                SUCCESS,
                'Просмотр записей журнала'
            )
            return self.ru.ok_response_dict(serializer.data)
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при получении записей журнала: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при получении записей журнала'
            )
