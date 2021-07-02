from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response

class Mail:
    def send_mail_to_user(to, subject, body):
        send_mail(
            f'{subject}',
            f'{body}',
            f'{settings.EMAIL_HOST_USER}',
            [f'{to}'],
            fail_silently=False
        )
        return Response({'result': f'{to}'})