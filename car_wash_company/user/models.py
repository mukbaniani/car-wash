from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, tel_number, password=None):
        if not email:
            raise ValueError('მეილი აუცილებელია')
        if not first_name:
            raise ValueError('სახელი აუცილებელია')
        if not last_name:
            raise ValueError('გვარი აუცილებელია')
        if not tel_number:
            raise ValueError('ტელეფონის ნომერი აუცილებელია')
        user = self.model(
            email = self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            tel_number=tel_number
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.model(
            email = self.normalize_email(email)
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=15, verbose_name=_('სახელი'))
    last_name = models.CharField(max_length=15, verbose_name=_('გვარი'))
    email = models.EmailField(unique=True, verbose_name=_('მეილი'))
    tel_number = models.CharField(max_length=20, verbose_name=_('ტელეფონის ნომერი'))


    object = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('მომხმარებლები')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)