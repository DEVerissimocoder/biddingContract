from django.apps import AppConfig
from django.contrib.auth.signals import user_logged_in


class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios'

    def ready(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        from django.db.models.signals import post_save

        # Importando o sinal para enviar o email de boas-vindas
        from .signals import send_welcome_email
        post_save.connect(receiver=send_welcome_email, sender=User)

        # Importando o sinal para registrar o login do usuário
        from .signals import log_user_login
        user_logged_in.connect(receiver=log_user_login)