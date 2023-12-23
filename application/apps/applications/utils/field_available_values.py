import uuid
from typing import Optional

from apps.applications.models import FieldAvailableValues


class FieldAvailableValuesUtils:
    """Класс методов для работы с возможными значениями поля формы заявки"""

    @staticmethod
    def get_all_available_values():
        """Получение всех возможных значений из БД"""
        return FieldAvailableValues.objects.all()

    @staticmethod
    def get_available_values_for_field(field_id: uuid) -> Optional[FieldAvailableValues]:
        """Получение списка возможных значений для поля по его object_id"""
        try:
            return FieldAvailableValues.objects.filter(field_id=field_id).order_by('date_create')
        except Exception:
            return None

    @staticmethod
    def get_available_value_by_object_id(value_id: uuid) -> Optional[FieldAvailableValues]:
        """Получение возможного значения по object_id"""
        try:
            return FieldAvailableValues.objects.get(object_id=value_id)
        except Exception:
            return None

    @staticmethod
    def delete_available_value_by_object_id(value_id: uuid) -> Optional[str]:
        """Удаление возможного значения поля по полученному object_id"""
        try:
            field = FieldAvailableValues.objects.get(object_id=value_id)
            option = field.option
            field.delete()
            return option
        except Exception:
            return None
