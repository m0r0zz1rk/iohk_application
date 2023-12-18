from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.admins.filters.guides.participant_categories_filter import ParticipantCategoriesFilter
from apps.admins.serializers.guides.participant_categories_serializer import ParticipantCategoriesSerializer, \
    ParticipantCategoriesPaginationSerializer, ParticipantCategoriesSaveSerializer
from apps.commons.consts.journals.journal_event_results import SUCCESS, ERROR
from apps.commons.consts.journals.journal_rec_types import ADMINS
from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.permissions.is_auth import IsAuth
from apps.commons.utils.data_types.dict import DictUtils
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.admins.utils.participant_category import ParticipantCategoryUtils
from apps.authen.utils.profile import ProfileUtils
from apps.journals.writer.journal_writer import JournalWriter


class ParticipantCategoriesViewSet(viewsets.ModelViewSet):
    """API для работы с категориями участников"""
    permission_classes = [IsAuth, IsAdministrators]
    queryset = ParticipantCategoryUtils.get_participant_categories()
    serializer_class = ParticipantCategoriesSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend,]
    filterset_class = ParticipantCategoriesFilter

    journal = JournalWriter(ADMINS)
    ru = ResponseUtils()
    du = DictUtils()
    pu = ProfileUtils()

    @swagger_auto_schema(
        tags=['Категории участников'],
        operation_description="Получение категорий участников",
        responses={
            '400': 'Ошибка при получении категорий участников: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': ParticipantCategoriesPaginationSerializer
        }
    )
    def list(self, request, *args, **kwargs):
        """Получение категорий участников"""
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
                'Просмотр категорий участников'
            )
            return self.ru.ok_response_dict(serializer.data)
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при получении категорий участников: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при получении категорий участников'
            )

    @swagger_auto_schema(
        tags=['Категории участников'],
        request_body=ParticipantCategoriesSaveSerializer,
        operation_description="Добавление категории участников",
        responses={
            '400': 'Ошибка при добавлении категории участников: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Категория участников успешно добавлена'
        }
    )
    def save(self, request, *args, **kwargs):
        try:
            data = {
                'name': request.data['name'],
                'group': ParticipantCategoryUtils.get_group_id_by_name(request.data['group'])
            }
            serialize = ParticipantCategoriesSaveSerializer(data=data)
            if serialize.is_valid(raise_exception=True):
                serialize.save()
                self.journal.write(
                    self.pu.get_display_name('django_user_id', request.user.id),
                    SUCCESS,
                    f'Добавлена новая категория участников: '
                    f'{self.du.get_str_value_in_dict_by_key(
                        'name',
                        request.data
                    )}'
                )
                return self.ru.ok_response('Категория участников успешно добавлена')
            else:
                self.journal.write(
                    'Система',
                    ERROR,
                    f'Ошибка при добавлении категории участников: {serialize.errors}'
                )
                return self.ru.bad_request_response(serialize.errors)
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при добавлении категории участников: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.sorry_try_again_response()

    @swagger_auto_schema(
        tags=['Категории участников'],
        request_body=ParticipantCategoriesSaveSerializer,
        operation_description="Изменение категории участников",
        responses={
            '400': 'Ошибка при изменении категории участников: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Категория участников успешно изменена'
        }
    )
    def edit(self, request, *args, **kwargs):
        try:
            part_cat = ParticipantCategoryUtils.get_participant_category_by_object_id(self.kwargs['object_id'])
            data = {
                'name': request.data['name'],
                'group': ParticipantCategoryUtils.get_group_id_by_name(request.data['group'])
            }
            print(data)
            serialize = ParticipantCategoriesSaveSerializer(part_cat, data=data, partial=True)
            if serialize.is_valid(raise_exception=True):
                serialize.save()
                self.journal.write(
                    self.pu.get_display_name('django_user_id', request.user.id),
                    SUCCESS,
                    f'Изменена категория участников: '
                    f'{DictUtils().get_str_value_in_dict_by_key(
                        'name',
                        request.data
                    )}'
                )
                return self.ru.ok_response('Категория участников успешно изменена')
            else:
                self.journal.write(
                    'Система',
                    ERROR,
                    f'Ошибка при изменении категории участников: {serialize.errors}'
                )
                return self.ru.bad_request_response(serialize.errors)
        except Exception:
            error = ExceptionHandling.get_traceback()
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при изменении категории участников: {error}'
            )
            return self.ru.bad_request_response(error)

    @swagger_auto_schema(
        tags=['Категории участников'],
        operation_description="Удаление категории участников",
        responses={
            '400': 'Ошибка при удалении категории участников: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Категория участников успешно удалена'
        }
    )
    def delete(self, request, *args, **kwargs):
        try:
            name = ParticipantCategoryUtils.delete_participant_category_by_object_id(self.kwargs['object_id'])
            self.journal.write(
                self.pu.get_display_name('django_user_id', request.user.id),
                SUCCESS,
                f'Удалена категория участников: {name}'
            )
            return self.ru.ok_response('Категория участников успешно удалена')
        except Exception:
            error = ExceptionHandling.get_traceback()
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при удалении категории участников: {error}'
            )
            return self.ru.bad_request_response(error)
