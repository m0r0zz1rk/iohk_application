from apps.applications.models import AppFieldTypes


class AppFieldTypesUtils:
    """Класс методов для работы с типами полей заявок"""

    base_types = [
        {
            'alias': 'phone',
            'type': 'Номер телефона'
        },
        {
            'alias': 'profile_email',
            'type': 'Email (из профиля)'
        },
        {
            'alias': 'profile_age',
            'type': 'Возраст (из профиля)'
        },
        {
            'alias': 'date_range',
            'type': 'Временной интервал (дата-дата)'
        },
        {
            'alias': 'profile_birthday',
            'type': 'Дата рождения (из профиля)'
        },
        {
            'alias': 'date',
            'type': 'Дата'
        },
        {
            'alias': 'multiple',
            'type': 'Множественный выбор из списка'
        },
        {
            'alias': 'profile_oo_fullname',
            'type': 'Полное наименование ОО (из профиля)'
        },
        {
            'alias': 'profile_fio',
            'type': 'ФИО (из профиля)'
        },
        {
            'alias': 'text',
            'type': 'Текстовый'
        },
        {
            'alias': 'select',
            'type': 'Выбор из списка'
        },
        {
            'alias': 'profile_phone',
            'type': 'Номер телефона (из профиля)'
        },
        {
            'alias': 'number',
            'type': 'Числовой'
        },
        {
            'alias': 'email',
            'type': 'Email'
        },
        {
            'alias': 'profile_oo_shortname',
            'type': 'Краткое наименование ОО (из профиля)'
        },
    ]

    @staticmethod
    def get_all_types():
        """Получение всех типов полей"""
        return AppFieldTypes.objects.all().order_by('type')

    @staticmethod
    def check_types_exists() -> bool:
        """Проверка на наличие типов полей"""
        return AppFieldTypes.objects.exists()

    def add_base_field_types(self):
        """Добавление базовых типов полей в БД"""
        for field_type in self.base_types:
            print(field_type)
            new_type = AppFieldTypes(**field_type)
            new_type.save()
