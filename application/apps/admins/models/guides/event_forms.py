from django.db import models

from apps.commons.models import BaseTable


class EventForms(BaseTable):
    """Модель форм проведения мероприятий"""
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Наименование формы проведения мероприятия'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Форма проведения'
        verbose_name_plural = 'Формы проведения'
