DEFAULT = 'DEFAULT'
ADMINS = 'ADMINS'
APPLICATIONS = 'APPLICATIONS'
AUTHEN = 'AUTHEN'
STATES = 'STATES'
PROFILE = 'PROFILE'
CELERY_APP = 'CELERY_APP'
EVENTS = 'EVENTS'
JOURNALS = 'JOURNALS'
REPORTS = 'REPORTS'
USERS = 'USERS'

JOURNAL_REC_TYPES = (
    (DEFAULT, 'Не определено'),
    (ADMINS, 'Личный кабинет администратора'),
    (APPLICATIONS, 'Работа с заявками на мероприятия'),
    (AUTHEN, 'Авторизация/Регистрация'),
    (STATES, 'Работа с государствами'),
    (PROFILE, 'Работа с профилем пользователя'),
    (CELERY_APP, 'Работа с очередью задач Celery'),
    (EVENTS, 'Работа с мероприятиями'),
    (JOURNALS, 'Работа с журналами'),
    (REPORTS, 'Работа с отчетами'),
    (USERS, 'Личный кабинет пользователей')
)
