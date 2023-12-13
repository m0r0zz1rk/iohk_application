from django.db import models

from apps.commons.models import BaseTable


class ParticipantCategories(BaseTable):
    """Модель категорий участников"""
    name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        unique=True,
        verbose_name='Наименование категории участников'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория участников'
        verbose_name_plural = 'Категории участников'
