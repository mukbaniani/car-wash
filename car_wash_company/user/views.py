from django.http.response import HttpResponseRedirect
from .models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer, PasswordResetRequestSerializer, PasswordUpdateSerializer, RegisterSerializer
from rest_framework import generics, status, permissions
from .email import Mail
from .tokens import decode_reset_token
from django.contrib.sites.shortcuts import get_current_site


class RegisterUser(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)


class LoginUser(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        token, create = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class Logout(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordResetRequest(generics.CreateAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        Mail.send_password_reset_token(user.email, user.pk, request)
        return Response({'result': 'password reset token already sended'})


class PasswordUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = PasswordUpdateSerializer

    def get(self, request, *args, **kwargs):
        user_id = decode_reset_token(self.kwargs.get('uidb64'))
        currect_site = get_current_site(request)
        if not User.object.filter(pk=user_id).exists():
            return HttpResponseRedirect(f'http://{currect_site}/api/login/')
        else:
            return Response({'result': 'update your password'})


    def put(self, request, *args, **kwargs):
        user_id = decode_reset_token(self.kwargs.get('uidb64'))
        current_site = get_current_site(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(pk=user_id).first()
        password = serializer.validated_data.get('password1')
        try:
            user.set_password(password)
            user.save()
            return HttpResponseRedirect(f'http://{current_site}/api/login/')
        except:
            return Response({'result': 'პაროლის განსაახლებელ ტოკენს დრო გაუვიდა სცადეთ თავიდან'})