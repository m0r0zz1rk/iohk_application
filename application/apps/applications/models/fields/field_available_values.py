from django.db import models

from apps.applications.models import AppFields
from apps.commons.models import BaseTable


class FieldAvailableValues(BaseTable):
    """Модель возможных значений поля (для типа поля 'Выбор из списка')"""
    field = models.ForeignKey(
        AppFields,
        on_delete=models.CASCADE,
        null=True,
        default=None,
        verbose_name='Поле заявки'
    )
    option = models.CharField(
        max_length=500,
        null=False,
        blank=False,
        verbose_name='Возможное значение'
    )

    def __str__(self):
        return f'Варианта ответа "{self.option}" для поля "{self.field.name}"'

    class Meta:
        verbose_name = 'Возможное значение поля'
        verbose_name_plural = 'Возможные значение полей'
