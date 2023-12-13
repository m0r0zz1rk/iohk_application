from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.commons.consts.journals.journal_event_results import JOURNAL_EVENT_RESULTS, NONE
from apps.commons.consts.journals.journal_rec_types import JOURNAL_REC_TYPES
from apps.commons.models import BaseTable
from apps.commons.utils.django.django import DjangoUtils


class Journal(BaseTable):
    """Модель журнала событий"""
    event_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время фиксации события'
    )
    source = models.CharField(
        max_length=300,
        blank=False,
        null=False,
        verbose_name='Источник события'
    )
    rec_type = models.CharField(
        max_length=50,
        choices=JOURNAL_REC_TYPES,
        verbose_name='Тип события'
    )
    event_result = models.CharField(
        max_length=15,
        choices=JOURNAL_EVENT_RESULTS,
        default=NONE,
        verbose_name='Статус события'
    )
    description = models.TextField(
        max_length=10000,
        verbose_name='Детали события'
    )

    def __str__(self):
        return f'Запись журнала № {self.object_id} от {self.event_time.strftime('%d.%m.%Y %H:%M')}'

    class Meta:
        verbose_name = 'Запись журнала событий'
        verbose_name_plural = 'Записи журнала событий'


@receiver(post_save, sender=Journal)
def check_and_clear_journal(sender, **kwargs):
    """Проверка и очистка журнала в случае превышения максимального количества записей"""
    journal_max_length = DjangoUtils().get_parameter_from_settings('JOURNAL_MAX_LENGTH')
    if journal_max_length is not None:
        if Journal.objects.count() > journal_max_length:
            while Journal.objects.count() > journal_max_length:
                Journal.objects.all().order_by('date_create').first().delete()
