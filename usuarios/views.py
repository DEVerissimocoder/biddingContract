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
    success_mensage = "Cadastro feito com sucesso, entre em contato com o administrador do sistema e solicite a liberação!"

    def form_valid(self, form):
        form.instance.password = make_password(form.instance.password)
        form.instance.is_active = False
        form.save()
        messages.warning(self.request, self.success_mensage)
        return super(UserCreateView, self).form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    fields = ["username", "password"]
    redirect_authenticated_user = True
    success_message = "Usuário logado com sucesso!"
    error_message = "Erro de login: usuário não está ativo!"

    def form_valid(self, form):
        user = form.get_user()
        if user.is_active:
            messages.success(self.request, self.success_message)
            print(f"Veio aqui 111")
            print(messages.get_messages(self.request))
            return super(CustomLoginView, self).form_valid(form)
        else:
            messages.error(self.request, self.error_message)
            print(f"Entrou aqui")
            print(messages.get_messages(self.request))
            return self.form_invalid(form)

    def get_success_url(self):
        print("Aquiiiiiiiii")
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
    
    
# View para adicionar permissão ao usuário que fez o cadastro
def add_permission(request, pk):
    user = User.objects.get(pk=pk)
    user.is_active  = True
    user.save()
    return redirect("admin_users") 