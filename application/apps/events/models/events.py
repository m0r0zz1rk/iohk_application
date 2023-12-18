import datetime

from django.db import models

from apps.admins.models.guides.participant_categories import ParticipantCategories
from apps.commons.models import BaseTable
from apps.events.models.event_types import EventTypes


class Events(BaseTable):
    """Модель мероприятий"""
    name = models.CharField(
        max_length=500,
        null=False,
        blank=False,
        default='Новое мероприятие',
        verbose_name='Наименование мероприятия'
    )
    description = models.TextField(
        verbose_name='Краткое пояснение'
    )
    event_type = models.ForeignKey(
        EventTypes,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        verbose_name='Тип мероприятия'
    )
    app_date_start = models.DateField(
        default=datetime.date.today,
        verbose_name='Дата начала подачи заявок'
    )
    app_date_end = models.DateField(
        default=datetime.date.today,
        verbose_name='Дата окончания подачи заявок'
    )
    date_start = models.DateField(
        default=datetime.date.today,
        verbose_name='Дата начала проведения мероприятия'
    )
    date_end = models.DateField(
        default=datetime.date.today,
        verbose_name='Дата окончания проведения мероприятия'
    )
    categories = models.ManyToManyField(
        ParticipantCategories,
        default='Категории участников'
    )

    def __str__(self):
        return (f'{self.name} ({self.date_start.strftime('%d.%m.%Y')} - '
               f'{self.date_end.strftime('%d.%m.%Y')})')

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
