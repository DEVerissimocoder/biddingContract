from django.shortcuts import render
from django.http import HttpResponseRedirect
from  .forms import formLicitacao, formFornecedor
from django.urls import reverse
from .models import Licitacao, Fornecedor
# Create your views here.



def cadLicitacao(request):
    if (request.method == 'POST'):
        form = formLicitacao(request.POST)
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listLicitacoes'))
    else:
        form = formLicitacao()
    return render(request, 'biddingContracts/licitacao_new.html', {"form": form})

def listLicitacoes(request):
    """mostra todas as licitacoes"""
    licitacoes = Licitacao.objects.all()
    context = {"licitacoes": licitacoes}
   
    return render(request, "biddingContracts/licitacoes.html", context)
   

def cadFornecedor(request):
    if request.method == 'POST':
        form = formFornecedor(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listFornecedores'))
    else:
        form = formFornecedor()

    return render(request, 'biddingContracts/fornecedor_new.html', {"form": form})

def listFornecedores(request):
    """MOSTRA TODOS OS FORNECEDORES CADASTRADOS"""
    fornecedores = Fornecedor.objects.all()
    for fornecedor in fornecedores:
        print(fornecedor.nome)
    context = {"fornecedores": fornecedores}

    return render(request, "biddingContracts/fornecedores.html", context)
    
def index(request):
    return render(request, 'biddingContracts/index.html')


