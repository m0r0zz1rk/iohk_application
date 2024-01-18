from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from django.template.loader import render_to_string
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """Обработка поступившего запроса на изменение пароля"""
    # send an e-mail to the user
    context = {
        'reset_password_url': "{}?token={}".format(
            settings.AIS_ADDRESS+'password_reset',
            reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('email/password_reset_email.html', context)

    send_mail(
        "АИС подачи заявок ИОХК: Сброс пароля",
        None,
        settings.EMAIL_HOST_USER,
        [reset_password_token.user.email, ],
        fail_silently=False,
        html_message=email_html_message
    )
