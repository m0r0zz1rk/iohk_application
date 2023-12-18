import datetime

from django.db import models

from apps.commons.models import BaseTable
from apps.events.models import EventForms


class EventsSchedule(BaseTable):
    """Модель расписания мероприятия"""
    from apps.events.models.events import Events

    event = models.ForeignKey(
        Events,
        on_delete=models.CASCADE,
        null=True,
        default=None,
        verbose_name='Мероприятие'
    )
    start = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name='Время начала'
    )
    end = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name='Время окончания'
    )
    theme = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name='Тема'
    )
    form = models.ForeignKey(
        EventForms,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        verbose_name='Форма проведения'
    )
    url = models.URLField(
        null=True,
        blank=True,
        verbose_name='Ссылка'
    )
    address = models.TextField(
        null=True,
        blank=True,
        verbose_name='Адрес'
    )

    def __str__(self):
        return (f'Занятие мероприятия "{self.event.name}" с {self.start.strftime('%d.%m.%Y %H:%S')} до '
                f'{self.end.strftime('%d.%m.%Y %H:%S')}')

    class Meta:
        verbose_name = 'Расписание мероприятия'
        verbose_name_plural = 'Расписание мероприятий'
