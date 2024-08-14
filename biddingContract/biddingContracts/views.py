from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from  .forms import formLicitacao, formFornecedor, formContrato
from django.urls import reverse, reverse_lazy
from .models import Contrato, NotaFiscal, Fornecedor, Licitacao
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView

# CONTRATOS + RELATORIOS
def cadContrato(request):
    if request.method == "POST":
        form = formContrato(request.POST),

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("contratos"))
    else:
        form = formContrato()
    return render(request, "contrato_new.html", {"form": form})

def listContratos(request):
    contratos = Contrato.objects.all()
    context = {"contratos": contratos}
    return render(request, "contratos.html", context)

def contratosRelatorio(request, id_contrato):
    contrato = Contrato.objects.get(numero=id_contrato)
    notasFiscais = NotaFiscal.objects.filter(contrato_fk = id_contrato)
    saldoAtual = contrato.valor
    #tipo datetime.datetime
    hoje = datetime.today()
    # convertendo para o tipo datetime.date
    hoje = hoje.date()
    # tipo datetime.date
    dataFinalContrato = contrato.dataFinal  
    prazoRestante = relativedelta(dataFinalContrato, hoje)
    mensagem = verifica_prazo_validade_contrato(prazoRestante, dataFinalContrato, hoje)

    for notas in notasFiscais:
        if notas.contrato_fk.numero == contrato.numero:
            saldoAtual -= notas.valor
    context = {
        "notasfiscais": notasFiscais,
        "saldoAtual": saldoAtual,
        "vigencia": mensagem
        }
    return render(request, "contratos_relatorio.html", context)

def verifica_prazo_validade_contrato(prazoRestante, dataFinal, hoje):
    mensagem = " "
    if dataFinal >= hoje:
        mensagem = f"O contrato é válido por mais {prazoRestante.years} anos, {prazoRestante.months} meses e {prazoRestante.days} dias."
        return mensagem
    else:
        mensagem =  "O prazo de validade do contrato já expirou."
    return mensagem
# INDEX
def index(request):
    return render(request, 'index.html')


def listFornecedores(request):
    fornecedores = Fornecedor.objects.all()
    context = {"fornecedores": fornecedores}
    return render(request, "fornecedores.html", context)
"""
def infoFornecedores(request, forn_id):
  
    fornecedor = Fornecedor.objects.get(id = forn_id)
    
    context = {"fornecedor": fornecedor}

    return render(request, "biddingContracts/fornecedor.html", context)"""

def listLicitacoes(request):
    """mostra todas as licitacoes"""
    licitacoes = Licitacao.objects.all()
    context = {"licitacoes": licitacoes}
   
    return render(request, "list_licitacoes.html", context)

#View que cria as licitações
# @method_decorator(login_required(login_url=reverse_lazy("user:login")), name="dispatch")
# @method_decorator(user_complete_required, name="dispatch")

class BiddingCreateView(CreateView):
    """
    Faz o cadastro das licitações
    """
    model = Licitacao
    form_class = formLicitacao
    template_name = 'licitacoes.html'
    success_url = reverse_lazy('biddingContracts:licitacoes')
   