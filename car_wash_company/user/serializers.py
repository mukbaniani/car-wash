from rest_framework import serializers
from .models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(label=_('პაროლი'), write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(label=_('გაიმეორეთ პაროლი'), write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'tel_number', 'password1', 'password2']

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise serializers.ValidationError('პაროლი ერთმანეთს არ ემთხვევა')
        else:
            raise serializers.ValidationError('პაროლის ველის შევსება სავალდებულოა')
        return attrs

    def create(self, validated_data):
        password = self.validated_data.get('password1')
        user = User(
            first_name=self.validated_data.get('first_name'),
            last_name=self.validated_data.get('last_name'),
            email=self.validated_data.get('email'),
            tel_number=self.validated_data.get('tel_number'),
        )
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(label=_('პაროლი'), write_only=True, style={'input_type': 'password'})
    email = serializers.EmailField(label=_('მეილი'))
    token = serializers.CharField(label=_('token'), read_only=True)

    class Meta:
        model = User
        fields = ['password1', 'email', 'token']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password1')
        
        if email and password:
            user = authenticate(request=self.context.get('request'),
                    email=email, password=password)
            if not user:
                error_message = 'მეილი ან პაროლი არასწორია'
                raise serializers.ValidationError(error_message)
        else:
            error_message = 'მეილის და პაროლის შევსება სავალდებულოა'
            raise serializers.ValidationError(error_message)

        attrs['user'] = user
        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_('ემაილი'),
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        if email:
            user = User.object.filter(email=email).first()
            if not user:
                error_message = 'მეილი არ მოიძებნა'
                raise serializers.ValidationError(error_message)
        else:
            error_message = 'მეილის შეყვანა აუცილებელია'
            raise serializers.ValidationError(error_message)
        attrs['user'] = user
        return attrs


class PasswordUpdateSerializer(serializers.Serializer):
    password1 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        if password1 and password2:
            if password1 != password2:
                error_message = 'პაროლი არ ემთხვევა'
                raise serializers.ValidationError(error_message)
        else:
            error_message = 'პაროლის ველის შევსება აუცილებელია'
            raise serializers.ValidationError(error_message)
        return attrs