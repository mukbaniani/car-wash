from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Order
from .tasks import send_email


@receiver(post_save, sender=Order)
def send_email_to_user(sender, instance=None, created=False, **kwargs):
    if created:
        user_email = instance.user.email
        email_subject = 'თქვენი შეკვეთა წარმატებით განხორციელდა'
        email_body = f'გთხოვთ მობრძანდეთ {instance.order_date} -ს მისამართზე \n {instance.branch}'
        send_email.delay(
            user_email,
            email_subject,
            email_body
        )


@receiver(post_delete, sender=Order)
def send_delete_signal(sender, instance, using, **kwargs):
    user_email = instance.user.email
    email_subject = 'შეკვეთა წაშლილია'
    email_body = f'თქვენი შეკვეთა წაშლილია'
    send_email.delay(
        user_email,
        email_subject,
        email_body
    )