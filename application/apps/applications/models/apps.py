from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from tinymce import models as tinymce_models

from apps.applications.utils.app_fields import AppFieldsUtils
from apps.applications.utils.app_form_fields import AppFormFieldsUtils
from apps.authen.models import Profiles
from apps.commons.consts.apps.app_statuses import APP_STATUSES, DRAFT
from apps.commons.models import BaseTable
from apps.events.models import Events
from apps.events.utils.events_app_required import EventsAppsRequiredUtils


class Apps(BaseTable):
    """Модель заявок на участие в мероприятиях"""
    date_update = models.DateField(
        null=True,
        blank=True,
        default=None,
        verbose_name='Дата обновления'
    )
    profile = models.ForeignKey(
        Profiles,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        verbose_name='Профиль пользователя'
    )
    event = models.ForeignKey(
        Events,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Мероприятие'
    )
    status = models.CharField(
        max_length=30,
        choices=APP_STATUSES,
        default=DRAFT,
        verbose_name='Статус'
    )
    message = models.TextField(
        max_length=2000,
        verbose_name='Сообщение',
        blank=True
    )
    result = tinymce_models.HTMLField(
        blank=True,
        null=True,
        default='',
        verbose_name='Результат участия'
    )

    def __str__(self):
        if self.profile:
            display = self.profile.get_display_name()
        else:
            display = '(Данные не найдены)'
        return (f'Заявка от пользователя "{display}" на участие в мероприятии '
                f'"{self.event.name}" ({self.event.date_start.strftime("%d.%m.%Y")} - '
                f'{self.event.date_end.strftime("%d.%m.%Y")})')

    class Meta:
        verbose_name = 'Заявка на участие в мероприятие'
        verbose_name_plural = 'Заявки на участие в мероприятиях'


@receiver(post_save, sender=Apps)
def create_app_fields(instance, created, **kwargs):
    """Создание заполненных полей заявки пользователя при создании заявки"""
    if created:
        try:
            app_required = EventsAppsRequiredUtils.get_apps_required_for_event(instance.event_id)
            if app_required.user_app_required:
                fields = AppFieldsUtils.get_app_fields_for_event(instance.event_id, 'user_app')
                if fields is not None and fields.count() > 0:
                    for field in fields:
                        AppFormFieldsUtils.create_new_rec(
                            instance.object_id,
                            field.object_id,
                            True,
                            ''
                        )
        except Exception:
            pass
