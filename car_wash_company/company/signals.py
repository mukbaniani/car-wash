from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .emails import Mail

@receiver(post_save, sender=Order)
def send_email_to_user(sender, instance=None, created=False, **kwargs):
    if created:
        user = instance.user.email
        email_subject = 'თქვენი შეკვეთა წარმატებით განხორციელდა'
        email_body = f'გთხოვთ მობრძანდეთ {instance.order_date} -ს მისამართზე \n {instance.branch}'
        Mail.send_mail_to_user(
            user,
            email_subject,
            email_body
        )