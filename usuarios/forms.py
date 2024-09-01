from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()

class AccountSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
        ]

        labels = {
            "username": "Nome de Usuário",
            "email": "Digite o seu e-mail",
            "password": "Senha",
        }

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "type": "email",
                    "class": "form-control",
                }
            ),
            "password": forms.PasswordInput(
                attrs={
                    "type": "password",
                    "class": "form-control",
                }
            )
        }