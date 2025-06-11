from django.shortcuts import render, redirect
from usuarios.forms2 import  CadastroForms, CustomLoginForm, UpdateEmailForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages, auth
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import get_user_model
User = get_user_model()


def login(request):
    form = CustomLoginForm()

    if request.method == 'POST':
        form = CustomLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            usuario = authenticate(
                request,
                username=username,
                password=password
            )

            if usuario is not None and usuario.is_active:
                auth.login(request, usuario)
                messages.success(request, "Login Efetuado com sucesso!")
                return redirect('index')
            else:
                messages.error(request, "Usuário ou senha inválidos!")
                return redirect('login')
        else:
            messages.error(request, "Corrija os erros abaixo!")
    else:
        form = CustomLoginForm()
    
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
            print(form.errors, "kkkkkkkkk")
    
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
    
    

    
    
    
