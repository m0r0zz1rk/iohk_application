from apps.applications.models import AppFieldTypes


class AppFieldTypesUtils:
    """Класс методов для работы с типами полей заявок"""

    @staticmethod
    def get_all_types():
        """Получение всех типов полей"""
        return AppFieldTypes.objects.all().order_by('type')
