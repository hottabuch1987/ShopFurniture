from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string


@shared_task
def send_registration_email(username, email):
    subject = 'Добро пожаловать в нашу систему!'
    message = render_to_string('account/registration.html', {
        'username': username,
        'email': email,

    })
    send_mail(subject, None, 'varvar1987a@mail.ru', [email], [username], html_message=message)

