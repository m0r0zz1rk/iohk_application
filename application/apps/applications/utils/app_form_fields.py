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
                'user_form': user_form,
                'value': value
            }
            AppFormFields.objects.create(**data)
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
                        form_field = AppFormFields.objects.filter(app_id=app.object_id).\
                            filter(user_form=True).get(field_id=field.object_id)
                        info = {
                            'id': form_field.object_id,
                            'name': form_field.field.name,
                            'type': form_field.field.type.alias,
                            'value': form_field.value,
                            'options': []
                        }
                        if form_field.field.type.alias in ['select', 'multiple']:
                            available_values = FieldAvailableValuesUtils.get_available_values_for_field(field.object_id)
                            if available_values is not None:
                                info['options'] = [available.option for available in available_values]
                        form_fields.append(info)
            return form_fields
        except Exception:
            return None
