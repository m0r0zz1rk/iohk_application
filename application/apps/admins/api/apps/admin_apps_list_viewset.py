from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.admins.serializers.apps.admin_app_serializer import AdminAppsListSerializer
from apps.applications.utils.apps import AppsUtils
from apps.authen.utils.profile import ProfileUtils
from apps.commons.consts.journals.journal_event_results import SUCCESS, ERROR
from apps.commons.consts.journals.journal_rec_types import APPLICATIONS
from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.journals.writer.journal_writer import JournalWriter
from apps.users.filters.apps_filter import AppsFilter


class AdminAppsListViewSet(viewsets.ModelViewSet):
    """API для получения списка заявок"""
    permission_classes = [IsAuthenticated, IsAdministrators]
    queryset = AppsUtils.get_all_apps()
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = AppsFilter

    journal = JournalWriter(APPLICATIONS)
    ru = ResponseUtils()
    pu = ProfileUtils()

    @swagger_auto_schema(
        tags=['Заявки (ЛК администратора)'],
        operation_description="Получение списка заявок пользователя",
        responses={
            '400': 'Ошибка при получении списка. Повторите попытку позже',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': AdminAppsListSerializer(many=True)
        }
    )
    def get_apps_list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = AdminAppsListSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = AdminAppsListSerializer(queryset, many=True)
            self.journal.write(
                self.pu.get_display_name('django_user_id', request.user.id),
                SUCCESS,
                'Просмотр списка заявок'
            )
            return self.ru.ok_response_dict(serializer.data)
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при получении списка заявок: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.sorry_try_again_response()
