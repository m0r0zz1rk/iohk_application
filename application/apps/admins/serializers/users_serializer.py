from rest_framework import serializers

from apps.authen.models import Profiles, States
from apps.authen.serializers.profile_serializer import ProfileChangePasswordSerializer
from apps.authen.serializers.registration_serializer import RegistrationUniquePhoneSerializer, \
    RegistrationUniqueEmailSerializer
from apps.commons.serializers.pagination_serializer import PaginationSerializer


class UsersSerializer(serializers.ModelSerializer):
    """Сериализация данных профиля пользователя"""
    state = serializers.SlugRelatedField(
        slug_field='name',
        queryset=States.objects.all()
    )
    email = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField(label='Роль')

    def get_state(self, obj):
        """Получение названия государства"""
        return obj.state.name

    def get_email(self, obj):
        """Получение email пользователя"""
        return obj.django_user.email

    def get_role(self, obj):
        """Получение роли пользователя"""
        return obj.django_user.groups.first().name

    class Meta:
        model = Profiles
        fields = (
            'object_id',
            'state',
            'role',
            'surname',
            'name',
            'patronymic',
            'birthday',
            'age',
            'sex',
            'email',
            'phone',
            'oo_fullname',
            'oo_shortname'
        )


class UsersPaginationSerializer(PaginationSerializer):
    """Сериализация пагинационных данных пользователей"""
    results = UsersSerializer(many=True)


class UsersCheckPhoneSerializer(RegistrationUniquePhoneSerializer):
    """Сериализация данных при проверке уникального номера телефона"""
    object_id = serializers.UUIDField(
        allow_null=False,
        label='Object_id профиля пользователя'
    )


class UsersCheckEmailSerializer(RegistrationUniqueEmailSerializer):
    """Сериализация данных при проверке уникального email"""
    object_id = serializers.UUIDField(
        allow_null=False,
        label='Object_id профиля пользователя'
    )


class UserEditInfoSerializer(UsersSerializer):
    """Сериализация данных пользователя при изменении информации"""
    object_id = serializers.UUIDField(
        allow_null=False,
        label='Object_id профиля пользователя'
    )
    role = serializers.CharField(
        max_length=25,
        allow_null=False,
        allow_blank=False,
        label='Роль пользователя'
    )
    state = serializers.SerializerMethodField(
        label='Государство'
    )
    email = serializers.EmailField(
        allow_blank=False,
        allow_null=False
    )

    def get_state(self, obj):
        """Получение названия государства"""
        return obj.state.name


class UserChangePasswordSerializer(ProfileChangePasswordSerializer):
    """Сериализация данных при смене пароля пользователя из личного кабинета администраторы"""
    object_id = serializers.UUIDField(
        allow_null=False,
        label='Object_id профиля пользователя'
    )
