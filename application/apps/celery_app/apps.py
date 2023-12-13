from django.apps import AppConfig


class CeleryAppConfig(AppConfig):
    name = 'apps.celery_app'
    verbose_name = 'Приложение для работы с очередью задач Celery'
