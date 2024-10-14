from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios'

    def ready(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        from django.db.models.signals import post_save

        from .signals import send_welcome_email

        post_save.connect(receiver=send_welcome_email, sender=User)