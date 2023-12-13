from django.contrib import admin


from apps.authen.models import States, Profiles


@admin.register(States)
class StatesAdmin(admin.ModelAdmin):
    """Отображение модели государств в административной панели"""
    ordering = ('name',)


@admin.register(Profiles)
class ProfilesAdmin(admin.ModelAdmin):
    """Отображение модели профилей в административной панели"""
    list_display = (
        'state_name',
        'surname',
        'name',
        'patronymic',
        'birthday_str',
        'age',
        'get_sex',
        'get_email',
        'phone',
        'oo_shortname',
        'oo_fullname'
    )

    def state_name(self, obj):
        """Получение названия государства"""
        return obj.state.name

    def birthday_str(self, obj):
        """Получение даты рождения пользователя в формате дд.мм.гггг"""
        return obj.birthday.strftime('%d.%m.%Y')

    def get_sex(self, obj):
        """Получение пола пользователя"""
        if obj.sex is True:
            return 'М'
        return 'Ж'

    def get_email(self, obj):
        """Получение email пользователя"""
        return obj.django_user.email

    state_name.short_description = 'Государство'
    birthday_str.short_description = 'Дата рождения'
    get_sex.short_description = 'Пол'
    get_email.short_description = 'Email'
