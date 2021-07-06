from .manager import WasherManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Branch(models.Model):
    address = models.CharField(max_length=100, verbose_name=_('მისამართი'))
    work_days = models.CharField(max_length=60, verbose_name=_('სამუშაო დღეები'))
    tel_number = models.CharField(max_length=2, verbose_name=_('ტელეფონის ნომერი'))
    garage_amount = models.SmallIntegerField(verbose_name=_('ავტოფარეხის რაოდენობა'))


    class Meta:
        verbose_name = _('ფილიალები')

    def __str__(self):
        return self.address


class Washer(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('რომელ ფილიალში მუშაობს ?'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('მომხმარებელი'))
    part = models.PositiveSmallIntegerField(verbose_name=_('წილი 1 გარეცხილი მანქანიდან'))
    profite = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_free = models.BooleanField(default=True, verbose_name=_('თავისუფალია მრეცხავი ?'))
    objects = WasherManager()

    class Meta:
        verbose_name = _('მრეცხავები')

    def __str__(self):
        return f'{self.user}'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.user.is_washer = True
            self.user.save()
        super(Washer, self).save(*args, **kwargs)


class CarType(models.Model):
    car_type = models.CharField(max_length=30, verbose_name=_('მანქანის ტიპი'))
    wash_price = models.DecimalField(max_digits=4, decimal_places=2, verbose_name=_('გარეცხვის ღირებულება'))
    branch = models.ManyToManyField(Branch, verbose_name=_('რომელ ფილიალში რეცხავენ მანქანას'))

    class Meta:
        verbose_name = _('მანქანის ტიპები')

    def __str__(self):
        return self.car_type


class Order(models.Model):
    order_date = models.DateTimeField(verbose_name=_('შეკვეთის თარიღი'), default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('მომხმარებელი'))
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name=_('ფილიალი'))
    washer = models.ForeignKey(Washer, on_delete=models.CASCADE, verbose_name=_('მრეცხავი'))
    car_type = models.ForeignKey(CarType, on_delete=models.CASCADE, verbose_name=_('მანქანის ტიპი'))

    class Meta:
        verbose_name = _('შეკვეთები')

    def __str__(self):
        return f'{self.branch}'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.branch.garage_amount -= 1
            self.branch.save()
            self.washer.is_free = False
            self.washer.profite += self.car_type.wash_price * self.washer.part / 100
            self.washer.save()
        super(Order, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.pk:
            if self.washer.is_free is False:
                self.washer.profite -= self.car_type.wash_price * self.washer.part / 100
                self.washer.is_free = True
                self.washer.save()
        super(Order, self).delete(*args, **kwargs)