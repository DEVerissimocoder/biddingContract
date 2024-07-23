from django.shortcuts import render
from django.http import HttpResponseRedirect
from  .forms import formLicitacao, formFornecedor, formContrato
from django.urls import reverse
from .models import Licitacao, Fornecedor, Contrato, NotaFiscal
# Create your views here.


# LICITACÃO
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
   

# FORNECEDOR
def cadFornecedor(request):
    if request.method == 'POST':
        form = formFornecedor(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('fornecedores'))
    else:
        form = formFornecedor()

    return render(request, 'biddingContracts/fornecedor_new.html', {"form": form})

def listFornecedores(request):
    fornecedores = Fornecedor.objects.all()
    context = {"fornecedores": fornecedores}
    return render(request, "biddingContracts/fornecedores.html", context)
"""
def infoFornecedores(request, forn_id):
  
    fornecedor = Fornecedor.objects.get(id = forn_id)
    
    context = {"fornecedor": fornecedor}

    return render(request, "biddingContracts/fornecedor.html", context)"""


# CONTRATO
def cadContrato(request):
    if request.method == "POST":
        form = formContrato(request.POST),

        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse("contratos"))
    else:
        form = formContrato()
    return render(request, "biddingContracts/contrato_new.html", {"form": form})

def listContratos(request):
    contratos = Contrato.objects.all()
    context = {"contratos": contratos}
    return render(request, "contratos.html", context)

def contratosRelatorio(request, id_contrato):
    contrato = Contrato.objects.get(numero=id_contrato)
    notasFiscais = NotaFiscal.objects.filter(contrato_fk = id_contrato)
    saldoAtual = contrato.valor
    for notas in notasFiscais:
        if notas.contrato_fk.numero ==contrato.numero:
            saldoAtual -= notas.valor
    context = {
        "notasfiscais": notasFiscais,
        "saldoAtual": saldoAtual
        }
    return render(request, "contratos_relatorio.html", context)

# INDEX
def index(request):
    return render(request, 'biddingContracts/index.html')

