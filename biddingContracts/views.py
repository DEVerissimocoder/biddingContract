from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import UpdateView
from datetime import datetime
from  biddingContracts.forms import formLicitacao, formFornecedor, formContrato
from django.urls import reverse, reverse_lazy
from .models import Contrato, NotaFiscal, Fornecedor, Licitacao
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib import messages

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

class BiddingFornecedor(CreateView):
    model = Fornecedor
    form_class = formFornecedor
    template_name = 'fornecedor_new.html'
    print("BiddingFornecedor")
    success_url = reverse_lazy('biddingContracts:fornecedores')


def listFornecedores(request):
    fornecedores = Fornecedor.objects.all()
    context = {"fornecedores": fornecedores}
    return render(request, "fornecedores.html", context)

def listLicitacoes(request):
    """mostra todas as licitacoes"""
    licitacoes = Licitacao.objects.all()
    context = {"licitacoes": licitacoes}
    return render(request, "list_licitacoes.html", context)

class BiddingCreateView(CreateView):
    """
    Faz o cadastro das licitações
    """
    model = Licitacao
    form_class = formLicitacao
    template_name = 'licitacoes.html'
    success_url = reverse_lazy('biddingContracts:licitacoes')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Licitação cadastrada com sucesso!')
        return response

    

class BuscarView(View):
    """
    Faz a o filtro por licitações baseando-se no n° do mês digitado, de 1 a 12. 
    """
    template_name = 'buscar.html'

    def get(self, request):
        if "buscar" in request.GET:
            mes_to_search = request.GET['buscar']
            if mes_to_search:
                try:
                    mes_to_search = int(mes_to_search)
                    if 1 <= mes_to_search <= 12:
                        biddings = Licitacao.objects.filter(date__month=mes_to_search)
                        context = {"licitacoes": biddings}
                    else:
                        context = {"error_message": "Mês inválido. Digite um número entre 1 e 12."}
                except ValueError:
                    context = {"error_message": "Mês inválido. Digite um número entre 1 e 12."}
            else:
                context = {"error_message": "Por favor, digite um mês válido."}
        else:
            context = {}
        return render(request, self.template_name, context)

 
 # View que atualiza os membros da integração

class BiddingUpdateView(UpdateView):
    model = Licitacao
    template_name = "licitacoes/edit_licitacoes.html"
    form_class = formLicitacao
    context_object_name = "licitacao"

    def get_object(self, queryset=None):
        non = Licitacao.objects.get(numProcess=self.kwargs.get('pk'))
        print(f"RRRRRRRR {self.kwargs.get('pk')}")
        return non

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {"form": form})

    def get_success_url(self):
        return reverse_lazy("biddingContracts:licitacoes")