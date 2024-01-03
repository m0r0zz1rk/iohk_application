from django.core.management.base import BaseCommand

from apps.applications.utils.app_field_types import AppFieldTypesUtils


class Command(BaseCommand):
    """Базовая команда для добавления базовых типов полей форм заявок"""

    def handle(self, *args, **options):
        aftu = AppFieldTypesUtils()
        if not aftu.check_types_exists():
            aftu.add_base_field_types()
