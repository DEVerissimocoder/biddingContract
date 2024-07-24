from django.shortcuts import render
#from django.http import HttpResponseRedirect
#from  .forms import formLicitacao, formFornecedor, formContrato
from django.urls import reverse
from .models import Contrato, NotaFiscal
import datetime
from datetime import date
# Create your views here.


def listContratos(request):
    contratos = Contrato.objects.all()
    context = {"contratos": contratos}
    return render(request, "contratos.html", context)

def contratosRelatorio(request, id_contrato):
    contrato = Contrato.objects.get(numero=id_contrato)
    notasFiscais = NotaFiscal.objects.filter(contrato_fk = id_contrato)
    
    saldoAtual = contrato.valor
    
    hoje = date.today()
    dataFinalContrato = contrato.dataFinal

    prazoRestante=verifica_prazo_validade_contrato(dataFinalContrato, hoje)

    for notas in notasFiscais:
        if notas.contrato_fk.numero == contrato.numero:
            saldoAtual -= notas.valor
    context = {
        "notasfiscais": notasFiscais,
        "saldoAtual": saldoAtual,
        "vigencia": prazoRestante
        }
    return render(request, "contratos_relatorio.html", context)

def verifica_prazo_validade_contrato(dataFinal, hoje):
    anoFinalContrato = dataFinal.year
    mesFinalContrato = dataFinal.month
    diaFinalContrato = dataFinal.day
    anoAtual = hoje.year
    mesAtual = hoje.month
    diaAtual = hoje.day
    dataFinalContrato_dateTime = datetime.datetime(anoFinalContrato, mesFinalContrato, diaFinalContrato)
    dataAtual_dateTime = datetime.datetime(anoAtual, mesAtual, diaAtual) 

    if dataFinalContrato_dateTime >= dataAtual_dateTime:
        return dataFinalContrato_dateTime - dataAtual_dateTime

    return f"contrato passou do prazo: {dataFinalContrato_dateTime.strftime("%d/%m/%Y")}"

# INDEX
def index(request):
    return render(request, 'index.html')