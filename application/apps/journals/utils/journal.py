from apps.journals.models import Journal


class JournalUtils:
    """Класс методов для работы с журналом"""

    @staticmethod
    def get_all_records():
        """Получение всех записей журнала"""
        return Journal.objects.all().order_by('-event_time')
