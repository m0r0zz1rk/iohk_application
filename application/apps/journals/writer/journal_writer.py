from apps.commons.consts.journals.journal_event_results import JOURNAL_EVENT_RESULTS, ERROR
from apps.commons.consts.journals.journal_rec_types import DEFAULT, JOURNAL_REC_TYPES, JOURNALS
from apps.commons.utils.django.exception import ExceptionHandling
from apps.journals.models import Journal


class JournalWriter:
    """Класс записи событий в журнал"""
    rec_type = DEFAULT

    def __init__(
            self,
            rec_type: JOURNAL_REC_TYPES,
    ):
        """Инициализация - получение источника, описания, типа и результата событий"""
        self.rec_type = rec_type

    def write(
            self,
            source: str,
            event_result: JOURNAL_EVENT_RESULTS,
            description: str,
    ):
        """Функция записи данных в журнал"""
        data = {}
        try:
            data = {
                'source': source,
                'rec_type': self.rec_type,
                'event_result': event_result,
                'description': description,
            }
            Journal.objects.create(**data)
        except Exception:
            error_data = {
                'source': 'Система',
                'rec_type': JOURNALS,
                'event_result': ERROR,
                'description': f'Произошла ошибка при внесении записи в журнал событий '
                               f'(полученные данные для внесения: {data}): '
                               f'{ExceptionHandling.get_traceback()}'
            }
            Journal.objects.create(**error_data)
