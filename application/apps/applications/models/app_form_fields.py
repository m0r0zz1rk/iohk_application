from django.db import models

from apps.commons.models import BaseTable


class AppFormFields(BaseTable):
    """Модель заполненных полей заявок"""
    app = models.ForeignKey(
        'applications.Apps',
        on_delete=models.CASCADE,
        null=True,
        default=None,
        verbose_name='Заявка'
    )
    field = models.ForeignKey(
        'applications.AppFields',
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        verbose_name='Поля формы заявки'
    )
    user_form = models.BooleanField(
        default=True,
        verbose_name='Поле заявки пользователя'
    )
    value = models.TextField(
        max_length=5000,
        blank=True,
        verbose_name='Значение'
    )

    def __str__(self):
        field = ''
        if self.field is not None:
            field = self.field.name
        app = ''
        if self.app is not None:
            app = self.app
        return f'Поле "{field}" {app}'

    class Meta:
        verbose_name = 'Заполненное поле заявки'
        verbose_name_plural = 'Заполненные поля заявок'
