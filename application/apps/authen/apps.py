from django.apps import AppConfig


class AuthenConfig(AppConfig):
    name = 'apps.authen'
    verbose_name = 'Приложение для регистрации и аутентификации пользователей АИС'

    def ready(self):
        import apps.authen.rest_password_signals
