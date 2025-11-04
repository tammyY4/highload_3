from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string


from celery import shared_task
from django.core.mail import send_mail
import logging
logger = logging.getLogger(__name__)


@shared_task
def send_registration_email(email, token):
    logger.info(f"Sending registration email to {email} with token {token}")
    subject = 'Регистрация в системе'
    message = f"Перейдите по ссылке: http://127.0.0.1:8000/set-password/{token}/"
    send_mail(subject, '', from_email=None, recipient_list=[email], html_message=message)


@shared_task
def send_reset_email(email, token):
    subject = 'Восстановление пароля'
    message = render_to_string('reset_email.html', {'token': token})
    send_mail(subject, '', from_email=None, recipient_list=[email], html_message=message)