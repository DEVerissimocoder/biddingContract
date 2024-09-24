from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView

from django.contrib.auth import get_user_model
User = get_user_model()

from usuarios.forms import AccountSignupForm

class UserCreateView(CreateView):
    model = User
    template_name = "registration/cadastro.html"
    form_class = AccountSignupForm
    success_url = reverse_lazy("usuarios:login")
    success_mensage = "Cadastro feito com sucesso!"

    def form_valid(self, form):
        form.instance.password = make_password(form.instance.password)
        form.save()
        messages.success(self.request, self.success_mensage)
        return super(UserCreateView, self).form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = ["username", "password"]
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, 'Erro de login: usuário ou senha inválidos!')
        return super(CustomLoginView, self).form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, 'Usuário logado com sucesso!')
        self.request.session['messages'] = messages.get_messages(self.request)
        return reverse_lazy('biddingContracts:index')  # redireciona para a página inicial após o login
    

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('biddingContracts:index')

    def get_next_url(self):
        messages.info(self.request, 'Você foi deslogado com sucesso!')
        return super(CustomLogoutView, self).get_next_url()
    
    

class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': 'devmarcelo.gus@gmail.com',  # substitua com o seu endereço de e-mail
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': 'registration/password_reset_email.html',
        }
        form.save(**opts)
        return super().form_valid(form)

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'