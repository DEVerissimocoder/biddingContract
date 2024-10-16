from django.shortcuts import render, redirect
from django. urls import reverse_lazy
from usuarios.forms2 import  CadastroForms, CustomLoginForm, UpdateEmailForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages, auth
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import get_user_model
User = get_user_model()


def login(request):
    form = CustomLoginForm()

    if request.method == 'POST':
        form = CadastroForms(request.POST)

        if form.is_valid():
            username = form["username"].value()
            password = form["password"].value()

            usuario = authenticate(
                request,
                username=username,
                password=password
            )
            if  usuario.is_active:
                aviso = 'Login efetuado com sucesso!'
                auth.login(request, usuario)
                messages.success(request, aviso)
                return redirect('index')  # Redireciona para a página inicial após login bem-sucedido
            else:
                aviso = 'Login inválido! Dados incorretos ou conta não ativada.'
                messages.error(request, aviso)
                return redirect('login')  # Redireciona para a view de login em caso de erro
    else:

        if not request.user.is_authenticated:
            messages.info(request, 'Por favor, faça login para acessar.')
        #messages.info(request, 'Por favor, faça login para acessar.')
    
    return render(request, "registration/login.html", {"form": form})


def cadastro(request):
    form = CadastroForms()

    if request.method == 'POST':
        form = CadastroForms(request.POST)

        if form.is_valid():
            
            nome = form.cleaned_data["nome_cadastro"]
            email = form.cleaned_data["email"]
            senha = form.cleaned_data["senha"]
            
            if User.objects.filter(username=nome).exists():
                return redirect('login')

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email já cadastrado, use outro!")
                return render(request, "registration/cadastro.html", {"form": form})


            usuario = User.objects.create_user(
                username=nome,
                email=email,
                password=senha
            )
            usuario.is_active = False
            usuario.save()
            aviso = 'Cadastro efetuado com sucesso!'
            aviso2 = 'Enviamos um e-mail com algumas informações inportantes, verifique a sua caixa de entrada!'
            messages.success(request, aviso)
            messages.warning(request, aviso2)
            return redirect('login')
        else:
            print(form.error_class, "kkkkkkkkk")
    
    return render(request, "registration/cadastro.html", {"form": form})


def logout(request):
    auth.logout(request)
    messages.success(request, "Deslogado com sucesso!")
    return redirect('login')



class ListMemberView(ListView, PermissionRequiredMixin):
    model = User
    template_name = "usuario/list_usuarios.html"
    context_object_name = "usuarios"
    permission_required = ["auth.view_user"]

    
class DetailMemberView(DetailView, PermissionRequiredMixin):
    model = User
    template_name = "usuario/detalhe_usuario.html"
    context_object_name = "usuario"
    permission_required = ["auth.view_user"]

    def get_object(self):
        # Exibe o usuário logado
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email_form'] = UpdateEmailForm(instance=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        email_form = UpdateEmailForm(request.POST, instance=user)

        if email_form.is_valid():
            user = self.request.user
            email_form.save()
            messages.success(request, "Dados atualizados com sucesso!")
            return redirect('usuarios:detail_member', user.pk)  # Redireciona após a atualização bem-sucedida

        messages.error(request, "Dados inválidos, por favor verifique os dados!")
        return self.render_to_response(self.get_context_data(email_form=email_form))
    
    

    
    
    
