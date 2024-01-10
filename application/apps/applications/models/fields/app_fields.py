from django.apps import apps
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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


@receiver(post_save, sender=AppFields)
def create_app_form_fields(instance, created, **kwargs):
    """Добавление записей в заполненные поля заявок пользователей при добавлении поля в форму заявки"""
    if created:
        apps_model = apps.get_model('applications', 'Apps')
        app_form_fields_model = apps.get_model('applications', 'AppFormFields')
        qs_apps = apps_model.objects.filter(event_id=instance.event_id)
        if qs_apps.count() > 0:
            for app in qs_apps:
                rec_ids = app_form_fields_model.objects.filter(app_id=app.object_id).values_list('rec_id', flat=True).distinct()
                for id in rec_ids:
                    if id != 0:
                        data = {
                            'app_id': app.object_id,
                            'field_id': instance.object_id,
                            'rec_id': id,
                            'value': ''
                        }
                        app_form_fields_model.objects.create(**data)
