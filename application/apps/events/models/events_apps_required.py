from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.commons.models import BaseTable
from apps.events.models import Events


class EventsAppsRequired(BaseTable):
    """
        Модель для определения необходимости заявки пользователя и заявок
        участников от пользователя для мероприятий
    """
    event = models.OneToOneField(
        Events,
        on_delete=models.CASCADE,
        null=True,
        default=None,
        verbose_name='Мероприятие'
    )
    user_app_required = models.BooleanField(
        default=True,
        verbose_name='Заявка пользователя'
    )
    participant_app_required = models.BooleanField(
        default=False,
        verbose_name='Заявки участников от пользователя'
    )

    def __str__(self):
        return (f'Определение необходимости заявкок для мероприятия "{self.event.name}"'
                f' ({self.event.date_start.strftime('%d.%m.%Y')} - {self.event.date_end.strftime('%d.%m.%Y')})')

    class Meta:
        verbose_name = 'Определение необходимости заявок'
        verbose_name_plural = 'Определения необходимости заявок'


@receiver(post_save, sender=Events)
def create_app_required(instance, created, **kwargs):
    """Создание записи определения необходимости заявок для нового мероприятия"""
    if created:
        EventsAppsRequired.objects.create(event_id=instance.object_id)
