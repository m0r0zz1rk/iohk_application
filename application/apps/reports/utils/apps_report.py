import uuid
from typing import Optional

from django.apps import apps


class AppsReportUtils:
    """Класс методов для работы с выгрузкой заявок на мероприятие"""

    apps_model = apps.get_model('applications', 'Apps')
    app_fields_model = apps.get_model('applications', 'AppFields')
    app_form_fields_model = apps.get_model('applications', 'AppFormFields')
    event_id = None
    apps_types = ''

    def __init__(self, event_id: uuid, apps_types: str):
        """
            Инициализация класса - установка object_id мероприятия, из которого будут
            выгружаться заявки, и типов выгружаемых заявок
        """
        self.event_id = event_id
        self.apps_types = apps_types

    def _get_fields_queryset(self, user_app: bool) -> Optional[apps.get_model('applications', 'AppFields')]:
        """Получение queryset с полями заявок"""
        try:
            return (self.app_fields_model.objects.filter(event_id=self.event_id).
                    filter(user_app=user_app)).order_by('date_create')
        except Exception:
            return None

    def _apps_header_row(self, user_app: bool) -> list:
        """Генерация строки заголовка листа с заявками"""
        header_row = []
        try:
            fields = self._get_fields_queryset(user_app)
            for index, field in enumerate(fields, start=1):
                header_row.append(
                    {
                        'row': 1,
                        'col': index,
                        'value': field.name,
                        'bold': True,
                        'width': 70,
                        'align_center': True
                    }
                )
        except Exception:
            pass
        return header_row

    def content_data(self) -> Optional[list]:
        """Заполнение листов данными из заявок"""
        try:
            excel = []
            fields = self._get_fields_queryset(False)
            content = self._apps_header_row(False)
            applications = (self.apps_model.objects.filter(event_id=self.event_id).
                            order_by('profile__surname', 'profile__name', 'profile__patronymic'))
            if self.apps_types in ['user', 'all']:
                for app_index, app in enumerate(applications, start=2):
                    for field_index, field in enumerate(fields, start=1):
                        value = ''
                        if self.app_form_fields_model.objects.filter(app_id=app.object_id). \
                                filter(field_id=field.object_id).exists():
                            value = self.app_form_fields_model.objects.filter(app_id=app.object_id). \
                                get(field_id=field.object_id).value
                        cell = {
                            'row': app_index,
                            'col': field_index,
                            'value': value,
                            'width': 70,
                            'align_center': True
                        }
                        content.append(cell)
                excel.append({
                    'title': 'Пользователи',
                    'sheet_data': content
                })
            if self.apps_types in ['part', 'all']:
                rows = self.app_form_fields_model.objects.filter(app_id=applications.first().object_id). \
                    filter(field_id=fields.first().object_id).values_list('rec_id', flat=True).distinct()
                counter = 0
                for app_index, app in enumerate(applications, start=2):
                    for row in rows:
                        if self.app_form_fields_model.objects.filter(app_id=app.object_id). \
                                filter(field_id=fields.first().object_id).filter(rec_id=row).exists():
                            for field_index, field in enumerate(fields, start=1):
                                value = ''
                                if self.app_form_fields_model.objects.filter(app_id=app.object_id). \
                                        filter(field_id=field.object_id).filter(rec_id=row).exists():
                                    value = self.app_form_fields_model.objects.filter(app_id=app.object_id). \
                                        filter(rec_id=row).get(field_id=field.object_id).value
                                cell = {
                                    'row': app_index + counter,
                                    'col': field_index,
                                    'value': value,
                                    'width': 70,
                                    'align_center': True
                                }
                                content.append(cell)
                            counter += 1
                    counter -= 1
                excel.append({
                    'title': 'Участники',
                    'sheet_data': content
                })
            return excel
        except Exception:
            return None
