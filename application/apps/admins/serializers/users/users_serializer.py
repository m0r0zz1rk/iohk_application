from rest_framework import serializers

from apps.authen.models import Profiles
from apps.commons.pagination_serializer import PaginationSerializer


class UsersSerializer(serializers.ModelSerializer):
    """Сериализация данных профиля пользователя"""
    email = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField(label='Роль')

    def get_email(self, obj):
        return obj.django_user.email

    def get_role(self, obj):
        return obj.django_user.groups.first().name

    class Meta:
        model = Profiles
        fields = (
            'role',
            'state',
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
