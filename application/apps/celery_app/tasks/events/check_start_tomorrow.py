import datetime

from django.apps import apps
from django.conf import settings
from django.core.mail import send_mail

from apps.celery_app.utils import UserEventEmailsUtils
from apps.commons.consts.journals.journal_event_results import ERROR
from apps.commons.consts.journals.journal_rec_types import CELERY_APP
from apps.commons.utils.django.exception import ExceptionHandling
from apps.events.utils.events import EventsUtils
from apps.journals.writer.journal_writer import JournalWriter
from web_app.init_celery import app

apps_model = apps.get_model('applications', 'Apps')


@app.task
def check_start_tomorrow_task():
    """Проверка на наличие мероприятий, которые начинаются завтра,
        и отправка сообщений пользователям"""
    try:
        events = EventsUtils.get_list_of_start_tomorrow_events()
        count = 0
        if events.count() > 0:
            for event in events:
                tomorrow = datetime.date.today() + datetime.timedelta(days=1)
                subject = 'АИС подачи заявок ИОХК: Начало мероприятия состоится завтра'
                text = (f'<br>Завтра, {tomorrow.strftime('%d.%m.%Y')}, состоится начало мероприятия '
                        f'типа <b>{event.event_type.name}</b> под названием <b>"{event.name}"</b>.<br>'
                        f'Сроки проведения мероприятия: <b>{event.date_start.strftime('%d.%m.%Y')}-'
                        f'{event.date_end.strftime('%d.%m.%Y')}</b>')
                apps = apps_model.objects.filter(event_id=event.object_id)
                if apps.count() > 0:
                    for app in apps:
                        if not UserEventEmailsUtils.check_event_start_tomorrow(
                            app.profile.django_user_id,
                            event.object_id
                        ):
                            UserEventEmailsUtils.create_rec_event(
                                app.profile.django_user_id,
                                event.object_id,
                                'TOMORROW'
                            )
                            profile = app.profile
                            if profile is not None:
                                appeal = 'Уважаемая'
                                if profile.sex:
                                    appeal = 'Уважаемый'
                                message = f'{appeal} {profile.get_display_name()}!\n{text}'
                                send_mail(
                                    subject,
                                    None,
                                    settings.EMAIL_HOST_USER,
                                    [app.profile.django_user.email, ],
                                    fail_silently=False,
                                    html_message=message
                                )
                                count += 1
        return f'Выполнено, количество отправленных писем: {count}'
    except Exception:
        journal = JournalWriter(CELERY_APP)
        journal.write(
            'Celery',
            ERROR,
            f'Ошибка при отправки сообщений о завтрашнем начале мероприятия: '
            f'{ExceptionHandling.get_traceback()}'
        )
        return f'Ошибка: {ExceptionHandling.get_traceback()}'

