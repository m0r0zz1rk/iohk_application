from django.db import models

from apps.commons.models import BaseTable


class AppFieldTypes(BaseTable):
    """Модель типов полей форм заявки"""
    alias = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        unique=True,
        verbose_name='Алиас'
    )
    type = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        unique=True,
        verbose_name='Тип'
    )

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Тип поля'
        verbose_name_plural = 'Типы полей'
