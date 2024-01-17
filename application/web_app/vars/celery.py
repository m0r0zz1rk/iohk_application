from .email import *
from kombu.serialization import registry

CELERY_IMPORTS = ("apps.celery_app.tasks", )
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json', 'application/text', 'web_app/json']

registry.enable('json')
registry.enable('application/text')
registry.enable('web_app/json')
