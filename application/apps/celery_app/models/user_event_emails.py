from django.contrib.auth.models import User
from django.db import models

from apps.commons.models import BaseTable
from apps.events.models import Events


class UserEventEmails(BaseTable):
    """Таблица проверки отправленных пользователю сообщений по мероприятиям"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        default=None,
        verbose_name='Пользователь Django'
    )
    event = models.ForeignKey(
        Events,
        on_delete=models.CASCADE,
        null=True,
        default=None,
        verbose_name='Мероприятие'
    )
    event_published = models.BooleanField(
        default=False,
        verbose_name='Сообщение об опубликованном мероприятии'
    )
    event_start_tomorrow = models.BooleanField(
        default=False,
        verbose_name='Сообщение о начала мероприятия (завтра)'
    )
    event_start = models.BooleanField(
        default=False,
        verbose_name='Сообщение о начала мероприятия (сегодня)'
    )

    def __str__(self):
        return str(self.object_id)

    class Meta:
        verbose_name = 'Запись с проверкой почты по мероприятиям'
        verbose_name_plural = 'Записи с проверкой почты по мероприятиям'
