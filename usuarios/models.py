from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

def send_welcome_email(sender, instance, created, **kwargs):
    if created and instance.email:
        send_mail(
            "Boas Vindas",
            "Seja bem vindo ao nosso sistema",
            "devmarcelo.gus@gmail.com",
            [instance.email],
        )
