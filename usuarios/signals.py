from django.core.mail import send_mail


def send_welcome_email(sender, instance, created, **kwargs):
    if created and instance.email:
        send_mail(
            "Boas Vindas",
            "Seja bem vindo ao nosso sistema! Estamos muito felizes em saber que se cadastrou na nossa plataforma. Entre em contato com o administrador para a liberação da sua conta! ",
            "devmarcelo.gus@gmail.com",
            [instance.email],
        )