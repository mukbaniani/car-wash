from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .emails import Mail


@shared_task
def send_email(to, subject, body):
    Mail.send_mail_to_user(to, subject, body)
