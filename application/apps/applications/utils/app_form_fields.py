import uuid
from typing import Optional

from django.apps import apps

from apps.applications.models import AppFormFields
from apps.applications.utils.app_fields import AppFieldsUtils
from apps.applications.utils.field_available_values import FieldAvailableValuesUtils
from apps.events.utils.events_app_required import EventsAppsRequiredUtils


class AppFormFieldsUtils:
    """Класс методов для работы с заполненными полями заявок"""

    @staticmethod
    def create_new_rec(
            app_id: uuid,
            field_id: uuid,
            user_form: bool,
            value: str
    ) -> bool:
        """Создание заполненного поля заявки"""
        try:
            data = {
                'app_id': app_id,
                'field_id': field_id,
                'rec_id': 0,
                'value': value
            }
            if not user_form:
                data['rec_id'] = 1
            new_form_field = AppFormFields(**data)
            new_form_field.save()
            return True
        except Exception:
            return False

    @staticmethod
    def get_user_form_fields_for_app(profile_id: uuid, event_id: uuid) -> Optional[list]:
        """Получение заполненных полей заявки пользователя"""
        try:
            apps_model = apps.get_model('applications', 'Apps')
            form_fields = []
            app_required = EventsAppsRequiredUtils.get_apps_required_for_event(event_id)
            if app_required.user_app_required:
                app = apps_model.objects.filter(profile_id=profile_id).get(event_id=event_id)
                fields = AppFieldsUtils.get_app_fields_for_event(event_id, 'user_app')
                if fields is not None and fields.count() > 0:
                    for field in fields:
                        if AppFormFields.objects.filter(app_id=app.object_id).filter(field_id=field.object_id).exists():
                            form_field = AppFormFields.objects.filter(app_id=app.object_id).get(
                                field_id=field.object_id)
                            info = {
                                'object_id': form_field.object_id,
                                'name': form_field.field.name,
                                'type': form_field.field.type.alias,
                                'value': form_field.value,
                                'options': []
                            }
                            if form_field.field.type.alias in ['select', 'multiple']:
                                available_values = FieldAvailableValuesUtils.get_available_values_for_field(
                                    field.object_id)
                                if available_values is not None:
                                    info['options'] = [available.option for available in available_values]
                            form_fields.append(info)
            return form_fields
        except Exception:
            return None

    @staticmethod
    def get_user_form_fields_for_app_by_app_id(app_id: uuid) -> Optional[list]:
        """Получение заполненных полей заявки пользователя по ее Object_id"""
        try:
            apps_model = apps.get_model('applications', 'Apps')
            app = apps_model.objects.get(object_id=app_id)
            form_fields = []
            app_required = EventsAppsRequiredUtils.get_apps_required_for_event(
                app.event_id
            )
            if app_required.user_app_required:
                fields = AppFieldsUtils.get_app_fields_for_event(app.event_id, 'user_app')
                if fields is not None and fields.count() > 0:
                    for field in fields:
                        if AppFormFields.objects.filter(app_id=app.object_id).filter(field_id=field.object_id).exists():
                            form_field = AppFormFields.objects.filter(app_id=app.object_id).get(
                                field_id=field.object_id)
                            info = {
                                'object_id': form_field.object_id,
                                'name': form_field.field.name,
                                'type': form_field.field.type.alias,
                                'value': form_field.value,
                                'options': []
                            }
                            if form_field.field.type.alias in ['select', 'multiple']:
                                available_values = FieldAvailableValuesUtils.get_available_values_for_field(
                                    field.object_id)
                                if available_values is not None:
                                    info['options'] = [available.option for available in available_values]
                            form_fields.append(info)
            return form_fields
        except Exception:
            return None

    @staticmethod
    def get_part_form_recs_for_app(profile_id: uuid, event_id: uuid) -> Optional[list]:
        """Получение списка записей заполненных полей заявок участников от пользователя"""
        try:
            apps_model = apps.get_model('applications', 'Apps')
            form_fields = []
            app_required = EventsAppsRequiredUtils.get_apps_required_for_event(event_id)
            if app_required.participant_app_required:
                app = apps_model.objects.filter(profile_id=profile_id).get(event_id=event_id)
                fields = AppFieldsUtils.get_app_fields_for_event(event_id, 'part_app')
                if fields is not None and fields.count() > 0:
                    recs_exist = None
                    for field in fields:
                        if (AppFormFields.objects.filter(app_id=app.object_id).
                                filter(field_id=field.object_id).
                                filter(rec_id__gt=0).
                                exists()):
                            recs_exist = field.object_id
                            break
                    if recs_exist is not None:
                        recs_numbers = (AppFormFields.objects.filter(app_id=app.object_id).
                                        filter(field_id=recs_exist).
                                        filter(rec_id__gt=0).values_list('rec_id', flat=True).distinct().order_by('rec_id'))
                        for number in recs_numbers:
                            rec_info = {
                                'rec_id': number
                            }
                            rec_fields = []
                            for field in fields:
                                app_form_field = (AppFormFields.objects.filter(app_id=app.object_id).
                                                 filter(field_id=field.object_id).
                                                 get(rec_id=number))
                                field_info = {
                                    'field_id': field.object_id,
                                    'form_field_id': app_form_field.field_id,
                                    'value': app_form_field.value
                                }
                                rec_fields.append(field_info)
                            rec_info['fields'] = rec_fields
                            form_fields.append(rec_info)
            return form_fields
        except Exception:
           return None

    @staticmethod
    def get_part_form_recs_for_app_by_app_id(app_id: uuid) -> Optional[list]:
        """Получение списка записей заполненных полей заявок участников от пользователя по Object_id заявки"""
        try:
            apps_model = apps.get_model('applications', 'Apps')
            event_id = apps_model.objects.get(object_id=app_id).event_id
            profile_id = apps_model.objects.get(object_id=app_id).profile_id
            form_fields = []
            app_required = EventsAppsRequiredUtils.get_apps_required_for_event(event_id)
            if app_required.participant_app_required:
                app = apps_model.objects.filter(profile_id=profile_id).get(event_id=event_id)
                fields = AppFieldsUtils.get_app_fields_for_event(event_id, 'part_app')
                if fields is not None and fields.count() > 0:
                    recs_exist = None
                    for field in fields:
                        if (AppFormFields.objects.filter(app_id=app.object_id).
                                filter(field_id=field.object_id).
                                filter(rec_id__gt=0).
                                exists()):
                            recs_exist = field.object_id
                            break
                    if recs_exist is not None:
                        recs_numbers = (AppFormFields.objects.filter(app_id=app.object_id).
                                        filter(field_id=recs_exist).
                                        filter(rec_id__gt=0).values_list('rec_id', flat=True).distinct().order_by(
                            'rec_id'))
                        for number in recs_numbers:
                            rec_info = {
                                'rec_id': number
                            }
                            rec_fields = []
                            for field in fields:
                                app_form_field = (AppFormFields.objects.filter(app_id=app.object_id).
                                                  filter(field_id=field.object_id).
                                                  get(rec_id=number))
                                field_info = {
                                    'field_id': field.object_id,
                                    'form_field_id': app_form_field.field_id,
                                    'value': app_form_field.value
                                }
                                rec_fields.append(field_info)
                            rec_info['fields'] = rec_fields
                            form_fields.append(rec_info)
            return form_fields
        except Exception:
            return None

    @staticmethod
    def add_new_form_field(app_field):
        """Добавление во все заявки пользователей на мероприятие нового поля формы"""
        try:
            apps_model = apps.get_model('applications', 'Apps')
            qs_apps = apps_model.objects.filter(event_id=app_field.event_id)
            if qs_apps.count() > 0:
                for app in qs_apps:
                    data = {
                        'app_id': app.object_id,
                        'field_id': app_field.object_id,
                        'user_form': app_field.user_app,
                        'value': ''
                    }
                    AppFormFields.objects.create(**data)
        except Exception:
            pass

    @staticmethod
    def save_field_value(field_id: uuid, value: str) -> bool:
        """Сохранение значения поля"""
        try:
            field = AppFormFields.objects.get(object_id=field_id)
            field.value = value
            field.save()
            return True
        except Exception:
            return False

    @staticmethod
    def save_part_app_rec(profile_id: uuid, event_id: uuid, rec_id: int, fields: list) -> bool:
        """Сохранение заявки участника от пользователя"""
        try:
            apps_model = apps.get_model('applications', 'Apps')
            app = apps_model.objects.filter(profile_id=profile_id).get(event_id=event_id)
            for field_dict in fields:
                new_rec = AppFormFields(
                    app_id=app.object_id,
                    field_id=field_dict['field_id'],
                    rec_id=rec_id,
                    value=field_dict['value']
                )
                new_rec.save()
            return True
        except Exception:
            return False

    @staticmethod
    def edit_part_app_rec(profile_id: uuid, event_id: uuid, rec_id: int, fields: list) -> bool:
        """Изменение заявки участника от пользователя"""
        try:
            apps_model = apps.get_model('applications', 'Apps')
            app = apps_model.objects.filter(profile_id=profile_id).get(event_id=event_id)
            form_fields = AppFormFields.objects.filter(app_id=app.object_id).filter(rec_id=rec_id)
            for form_field in form_fields:
                for field_dict in fields:
                    if field_dict['field_id'] == str(form_field.field_id):
                        form_field.value = field_dict['value']
                        form_field.save()
                        break
            return True
        except Exception:
            return False

    @staticmethod
    def del_part_app_rec(profile_id: uuid, event_id: uuid, rec_id: int) -> bool:
        """Удаление заявки участника от пользователя"""
        try:
            apps_model = apps.get_model('applications', 'Apps')
            app = apps_model.objects.filter(profile_id=profile_id).get(event_id=event_id)
            form_fields = AppFormFields.objects.filter(app_id=app.object_id).filter(rec_id=rec_id)
            for form_field in form_fields:
                form_field.delete()
            return True
        except Exception:
            return False

    @staticmethod
    def get_dunder_str_field(field_id: uuid) -> Optional[str]:
        """Получение текстового значения заполненного поля заявки"""
        try:
            field = AppFormFields.objects.get(object_id=field_id)
            return field.field.__str__
        except Exception:
            return None
