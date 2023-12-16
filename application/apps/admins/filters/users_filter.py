from django.contrib.auth.models import User, Group
from django_filters import rest_framework as filters
from django_filters import filters as df_filters

from apps.authen.models import Profiles


class UsersFilter(filters.FilterSet):
    """Поля для фильтрации пользователей"""
    role = filters.CharFilter(method='filter_role')
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

    def filter_role(self, queryset, name, value):
        if not value or value == '':
            return queryset
        group = Group.objects.get(name=value)
        print(group)
        users_ids = [user.id for user in User.objects.all() if group.user_set.filter(id=user.id).exists()]
        queryset = Profiles.objects.filter(django_user_id__in=users_ids)
        return queryset

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
