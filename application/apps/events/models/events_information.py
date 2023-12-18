from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from tinymce import models as tinymce_models

from apps.commons.models import BaseTable
from apps.events.models import Events


class EventsInformation(BaseTable):
    """Класс информационных сообщений о мероприятий"""
    event = models.ForeignKey(
        Events,
        on_delete=models.CASCADE,
        null=True,
        default=None,
        verbose_name='Мероприятие'
    )
    info = tinymce_models.HTMLField(
        default='Стандартный текст сообщения',
        verbose_name='Информационное сообщение'
    )

    def __str__(self):
        return (f'Информационно сообщение мероприятия "{self.event.name}" '
                f'({self.event.date_start.strftime('%d.%m.%Y')} - '
                f'{self.event.date_end.strftime('%d.%m.%Y')})')

    class Meta:
        verbose_name = 'Информационное сообщение'
        verbose_name_plural = 'Информационные сообщения'


@receiver(post_save, sender=Events)
def create_events_information(instance, created, **kwargs):
    """Создание информационного сообщения при создании мероприятия"""
    if created:
        EventsInformation.objects.create(
            event_id=instance.object_id
        )
