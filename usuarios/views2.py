from django.shortcuts import render, redirect
from django. urls import reverse_lazy
from usuarios.forms2 import  CadastroForms, CustomLoginForm
from django.contrib.auth.models import User
from django.contrib import messages, auth


def login(request):
    form = CustomLoginForm()

    if request.method == 'POST':
        form = CustomLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            usuario = auth.authenticate(
                request,
                username=username,
                password=password
            )
            if usuario is not None and usuario.is_active:
                aviso = 'Login efetuado com sucesso!'
                messages.success(request, aviso)
                auth.login(request, usuario)
                return redirect('index.html')
            else:
                aviso = 'Login Inválido! Dados incorretos ou conta não ativada.'
                messages.error(request,aviso)
                return redirect('login.html')

    return render(request, "registration/login.html", {"form": form})

def cadastro(request):
    form = CadastroForms()

    if request.method == 'POST':
        form = CadastroForms(request.POST)

        if form.is_valid():
            
            nome = form["nome_cadastro"].value()
            email = form["email"].value()
            senha = form["senha"].value()
            
            if User.objects.filter(username=nome).exists():
                return redirect('login')

            usuario = User.objects.create_user(
                username=nome,
                email=email,
                password=senha
            )
            usuario.is_active = False
            usuario.save()
            aviso = 'Cadastro efetuado com sucesso!'
            messages.success(request, aviso)
            return redirect('login')

    return render(request, "registration/cadastro.html", {"form": form})


def logout(request):
    auth.logout(request)
    messages.success(request, "Deslogado com sucesso!")
    return redirect('login')


