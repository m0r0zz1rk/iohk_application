from django.db import models

from apps.commons.models import BaseTable


class EventTypes(BaseTable):
    """Модель типов мероприятий"""
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Наименование типа мероприятия'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип мероприятия'
        verbose_name_plural = 'Типы мероприятий'
