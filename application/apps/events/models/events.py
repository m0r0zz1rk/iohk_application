import datetime

from django.db import models

from apps.admins.models.guides.participant_categories import ParticipantCategories
from apps.commons.consts.events.event_statuses import EVENT_STATUSES, CREATED
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
        blank=True,
        verbose_name='Краткое пояснение'
    )
    event_type = models.ForeignKey(
        EventTypes,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        verbose_name='Тип мероприятия'
    )
    event_status = models.CharField(
        max_length=30,
        choices=EVENT_STATUSES,
        default=CREATED,
        verbose_name='Статус мероприятия'
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

    def check_date_in_app_dates(self) -> bool:
        """Проверка нахождения текущей даты в сроках подачи заявки"""
        if self.app_date_start <= datetime.date.today() <= self.app_date_end:
            return True
        return False

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
