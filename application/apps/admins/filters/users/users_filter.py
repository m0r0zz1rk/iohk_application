from django_filters import rest_framework as filters

from apps.authen.models import Profiles


class UsersFilter(filters.FilterSet):
    """Поля для фильтрации пользователей"""
    state = filters.CharFilter(
        field_name='state__name'
    )
    surname = filters.CharFilter(
        lookup_expr='icontains'
    )
    name = filters.CharFilter(
        lookup_expr='icontains'
    )
    patronymic = filters.CharFilter(
        lookup_expr='icontains'
    )
    email = filters.CharFilter(
        field_name='django_user__email',
        lookup_expr='icontains'
    )
    phone = filters.CharFilter(
        lookup_expr='icontains'
    )
    oo_fullname = filters.CharFilter(
        lookup_expr='icontains'
    )
    oo_shortname = filters.CharFilter(
        lookup_expr='icontains'
    )

    class Meta:
        model = Profiles
        fields = (
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
