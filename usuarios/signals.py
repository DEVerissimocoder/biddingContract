from django.core.mail import send_mail
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from biddingContracts.models import UserLogin


def send_welcome_email(sender, instance, created, **kwargs):
    if created and instance.email:
        send_mail(
            "Boas Vindas",
            "Seja bem vindo ao nosso sistema! Estamos muito felizes em saber que se cadastrou na nossa plataforma. Entre em contato com o administrador para a liberação da sua conta! ",
            "devmarcelo.gus@gmail.com",
            [instance.email],
        )

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    UserLogin.objects.create(user=user)