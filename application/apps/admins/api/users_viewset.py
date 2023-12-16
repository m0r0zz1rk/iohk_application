from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.admins.filters.users_filter import UsersFilter
from apps.admins.serializers.users_serializer import UsersSerializer, UsersPaginationSerializer, \
    UserEditInfoSerializer, UsersCheckPhoneSerializer, UsersCheckEmailSerializer, UserChangePasswordSerializer
from apps.commons.consts.journals.journal_event_results import SUCCESS, ERROR, INFO
from apps.commons.consts.journals.journal_rec_types import ADMINS
from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.permissions.is_auth import IsAuth
from apps.commons.utils.data_types.dict import DictUtils
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.commons.utils.django.rest import RestUtils
from apps.commons.utils.models.profile import ProfileUtils
from apps.journals.writer.journal_writer import JournalWriter


class UsersViewSet(viewsets.ModelViewSet):
    """API для работы с пользователями"""
    permission_classes = [IsAuth, IsAdministrators]
    queryset = ProfileUtils.get_all_profiles()
    serializer_class = UsersSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend,]
    filterset_class = UsersFilter

    journal = JournalWriter(ADMINS)
    ru = ResponseUtils()
    restu = RestUtils()
    du = DictUtils()
    pu = ProfileUtils()

    @swagger_auto_schema(
        tags=['Администрирование'],
        operation_description="Получение пользователей",
        responses={
            '400': 'Ошибка при получении списка пользователей: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': UsersPaginationSerializer,
        }
    )
    def list(self, request, *args, **kwargs):
        """Получение типов мероприятий"""
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
                'Просмотр пользователей'
            )
            return self.ru.ok_response_dict(serializer.data)
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при получении пользователей: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return self.ru.bad_request_response(
                f'Ошибка при получении пользователей'
            )

    @swagger_auto_schema(
        tags=['Администрирование', ],
        operation_description="Проверка на возможность смены номера телефона пользователя",
        request_body=UsersCheckPhoneSerializer,
        responses={
            '400': 'Ошибка при проверке',
            '200': 'Проверка пройдена - указанный номер телефона не используется другими пользователями'
        }
    )
    def check_change_phone(self, request, *args, **kwargs):
        """Проверка на другой профиль с полученным номером телефона"""
        params = ['phone', 'object_id']
        if not self.restu.validate_params_to_list(request, params):
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при проверке возможности смены номера телефона: '
                f'Ошибка валидации тела запроса"'
            )
            return ResponseUtils().sorry_try_again_response()
        try:
            if ProfileUtils.check_unique_phone(
                    self.restu.get_request_parameter_by_key(request, 'phone'),
                    self.pu.get_profile_info(
                        'object_id',
                        self.restu.get_request_parameter_by_key(request, 'object_id'),
                        'django_user_id'
                    )
            ):
                return ResponseUtils.ok_response_no_data()
            else:
                return ResponseUtils.bad_request_no_data()
        except Exception as e:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при проверке возможности смены номера телефона: {e}"'
            )
            return ResponseUtils().sorry_try_again_response()

    @swagger_auto_schema(
        tags=['Администрирование', ],
        operation_description="Проверка на возможность смены email пользователя",
        request_body=UsersCheckEmailSerializer,
        responses={
            '400': 'Ошибка при проверке',
            '200': 'Проверка пройдена - указанный email не используется другими пользователями'
        }
    )
    def check_change_email(self, request, *args, **kwargs):
        """Проверка на существующего пользователя с указанным email"""
        params = ['email', 'object_id']
        if not self.restu.validate_params_to_list(request, params):
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при проверке возможности смены email: Ошибка валидации тела запроса"'
            )
            return ResponseUtils().sorry_try_again_response()
        try:
            if ProfileUtils.check_unique_email(
                    self.restu.get_request_parameter_by_key(request, 'email'),
                    self.pu.get_profile_info(
                        'object_id',
                        self.restu.get_request_parameter_by_key(request, 'object_id'),
                        'django_user_id'
                    )
            ):
                return ResponseUtils.ok_response_no_data()
            else:
                return ResponseUtils.bad_request_no_data()
        except Exception as e:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при проверке возможности смены email: {e}"'
            )
            return ResponseUtils().sorry_try_again_response()

    @swagger_auto_schema(
        tags=['Администрирование'],
        request_body=UserEditInfoSerializer,
        operation_description="Изменение данных пользователя",
        responses={
            '400': 'Ошибка при изменении данных пользователя: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Данные пользователя успешно изменены'
        }
    )
    def edit(self, request, *args, **kwargs):
        try:
            profile = self.pu.get_profile_by_object_id(
                self.du.get_str_value_in_dict_by_key('object_id', request.data)
            )
            serialize = UserEditInfoSerializer(profile, data=request.data, partial=True)
            if serialize.is_valid(raise_exception=True):
                serialize.save()
                user_id = self.pu.get_profile_info(
                    'object_id',
                    serialize.data['object_id'],
                    'django_user_id'
                )
                changes = self.pu.change_profile_info(user_id, request.data)
                if changes is True:
                    if self.pu.change_user_role(
                            user_id,
                            request.data['role']
                    ):
                        self.journal.write(
                            self.pu.get_display_name('django_user_id', request.user.id),
                            SUCCESS,
                            f'Профиль пользователя успешно изменен'
                        )
                        return ResponseUtils.ok_response('Информация профиля успешно изменена')
                    else:
                        self.journal.write(
                            self.pu.get_display_name('django_user_id', request.user.id),
                            INFO,
                            f'Профиль пользователя успешно изменен, но роль не была изменена'
                        )
                        return ResponseUtils.ok_response('Информация профиля успешно изменена')
                self.journal.write(
                    self.pu.get_display_name('django_user_id', request.user.id),
                    SUCCESS,
                    f'Изменены данные пользователя: '
                    f'{self.pu.get_display_name('object_id', profile.object_id)}'
                )
                return self.ru.ok_response('Данные пользователя успешно изменены')
            else:
                self.journal.write(
                    'Система',
                    ERROR,
                    f'Ошибка при изменении данных пользователя: {serialize.errors}'
                )
                return self.ru.bad_request_response(serialize.errors)
        except Exception:
            error = ExceptionHandling.get_traceback()
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при изменении данных пользователя: {error}'
            )
            return self.ru.bad_request_response(error)

    @swagger_auto_schema(
        tags=['Администрирование', ],
        operation_description="Смена пароля пользователя",
        request_body=UserChangePasswordSerializer,
        responses={
            '400': 'Ошибка при попытке смены пароля',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Пароль успешно изменен'
        }
    )
    def change_user_password(self, request, *args, **kwargs):
        """Смена пароля пользователя"""
        params = ['password', 'object_id']
        ru = RestUtils()
        if not ru.validate_params_to_list(request, params):
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при изменении пароля пользователя : '
                f'Ошибка валидации тела запроса"'
            )
            return ResponseUtils().sorry_try_again_response()
        pu = ProfileUtils()
        if pu.change_user_password(
                self.pu.get_profile_info(
                    'object_id',
                    self.restu.get_request_parameter_by_key(request, 'object_id'),
                    'django_user_id'
                ),
                ru.get_request_parameter_by_key(request, 'password')
        ):
            self.journal.write(
                pu.get_display_name('django_user_id', request.user.id),
                SUCCESS,
                f'Пароль пользователя {self.pu.get_profile_info(
                        'object_id',
                        self.restu.get_request_parameter_by_key(request, 'object_id'),
                        'django_user_id'
                    )} успешно изменен'
            )
            return ResponseUtils.ok_response('Пароль успешно изменен')
        else:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при изменении пароля пользователя {self.pu.get_profile_info(
                        'object_id',
                        self.restu.get_request_parameter_by_key(request, 'object_id'),
                        'django_user_id'
                    )}'
            )
            return ResponseUtils().sorry_try_again_response()
