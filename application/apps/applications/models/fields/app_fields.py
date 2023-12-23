from django.db import models

from apps.applications.models.fields.app_field_types import AppFieldTypes
from apps.commons.models import BaseTable
from apps.events.models import Events


class AppFields(BaseTable):
    """Модель полей формы заявок для мероприятий"""
    event = models.ForeignKey(
        Events,
        on_delete=models.CASCADE,
        null=True,
        default=None,
        verbose_name='Мероприятие'
    )
    user_app = models.BooleanField(
        default=True,
        verbose_name='Поле заявки пользователей'
    )
    name = models.CharField(
        max_length=250,
        null=False,
        blank=False,
        default='(Новое поле)',
        verbose_name='Наименование поля'
    )
    type = models.ForeignKey(
        AppFieldTypes,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        verbose_name='Тип поля'
    )

    def __str__(self):
        return (f'Поле "{self.name}" для мероприятия "{self.event.name}" '
                f'({self.event.date_start.strftime('%d.%m.%Y')}) - '
                f'{self.event.date_end.strftime('%d.%m.%Y')})')

    class Meta:
        verbose_name = 'Поле формы заявки пользователей на мероприятие'
        verbose_name_plural = 'Поля формы заявки пользователей на мероприятия'
