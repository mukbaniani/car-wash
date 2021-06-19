from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
from .tokens import encode_reset_token
from django.contrib.sites.shortcuts import get_current_site


class Mail:
    def send_password_reset_token(to, user, request):
        current_site = get_current_site(request)
        send_mail(
            'reset password',
            f'click here to reset your password {current_site.domain}/api/update-password/{encode_reset_token(user)}',
            'zura.mukbaniani.11@gmail.com',
            [f'{to}'],
            fail_silently=False,
        )
        return Response({'result': 'reset token sended'}, status=status.HTTP_200_OK)