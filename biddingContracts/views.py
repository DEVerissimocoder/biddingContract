from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.views import View
from django.views.generic import UpdateView
from datetime import datetime
from django.db.models import Q
from  biddingContracts.forms import formLicitacao, formFornecedor, formContrato, formARP, NotaFiscalForm
from django.urls import reverse, reverse_lazy
from .models import Contrato, NotaFiscal, Fornecedor, Licitacao, AtaRegistroPreco
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from django.template.loader import render_to_string
from django.views.generic import CreateView, ListView
from django.contrib import messages
import tempfile
import weasyprint
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required


def cadContrato(request, fornecedor_id):
    if request.method == "POST":
        form = formContrato(request.POST)
        print(f"Dados recebidos no POST: {request.POST}") 
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("biddingContracts:contratos"))
        else:
            print(f"Deu errado!{form.errors}")
    
    # fluxo 2-> segunda requisição, ou seja, quando ele vem da tela de cadastro de fornecedor.
    if fornecedor_id!='0':
        #consulta o fornecedor vindo do banco através do ID e cria um objeto com os dados retornado da tabela fornecedor
        fornecedor = Fornecedor.objects.get(id = fornecedor_id)
        
        form = formContrato()
        context={'form':form, 'fornecedor_id':fornecedor.id}
        return render(request, 'contrato_new.html', context)
    
    # fluxo 1 -> primeira requisição get
    else:
        form = formContrato()
        context={'form':form,'fornecedor_id':fornecedor_id}
        return render(request, "contrato_new.html", context)
    

# def listContratos(request):
#     contratos = Contrato.objects.all()
#     context = {"contratos": contratos}
#     print("chamando view")
#     return render(request, "contratos.html", context)

class ListContractsView(ListView):
    """
    Classe destinada a listar os contratos criados
    """
    model = Contrato
    template_name = "contratos.html"
    context_object_name = "contratos"

    # Adicionando filtros ao object_list através do get_queryset
    def get_queryset(self):
        txt_contratos = self.request.GET.get("contratos")
        txt_assunto = self.request.GET.get("assunto")
        txt_fornecedor = self.request.GET.get("fornecedor")
        txt_licitacao = self.request.GET.get("licitacao")

        if txt_fornecedor:
            queryset = Contrato.objects.filter(fornecedor_fk__nome__icontains=txt_fornecedor)
            return queryset
        elif txt_licitacao:
            queryset = Contrato.objects.filter(licitacao_fk__numProcess__icontains=txt_licitacao)
            return queryset
        elif txt_contratos:
            queryset = Contrato.objects.filter(numero__icontains=txt_contratos)
            return queryset
        elif txt_assunto:
            queryset = Contrato.objects.filter(assuntoDetalhado__icontains=txt_assunto)
            return queryset
        else:
            queryset = Contrato.objects.all()
        return queryset

# View que atualiza os contratos
class ContractsUpdateView(UpdateView):
    """
    Classe destinada a atualizar os contratos já criados
    """
    model = Contrato
    template_name = "contratos/edit_contratos.html"
    form_class = formContrato
    context_object_name = "contrato"

    def form_valid(self, form):
        messages.success(self.request, 'Contrato editado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao editar Contrato. Verifique os campos do formulário.')
        return render(self.request, self.template_name, {"form": form})

    def get_success_url(self):
        return reverse_lazy("biddingContracts:contratos")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def contratosRelatorio(request, id_contrato):
    contrato = Contrato.objects.get(id=id_contrato)
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
        "vigencia": mensagem,
        "hoje": hoje,
        "dataFinal": dataFinalContrato,
        }
    return render(request, "contratos_relatorio.html", context)



def verifica_prazo_validade_contrato(prazoRestante, dataFinal, hoje):
    mensagem = " "
    if dataFinal > hoje:
        mensagem = f"O contrato é válido por mais {prazoRestante.years} anos, {prazoRestante.months} meses e {prazoRestante.days} dias."
        return mensagem
    elif dataFinal == hoje:
        mensagem = f"O contrato é válido até hoje dia: {dataFinal.strftime('%d/%m/%y')}"
        return mensagem
    elif dataFinal < hoje:
        mensagem =  "O prazo de validade do contrato já expirou."
    return mensagem

def verifica_prazo_validade_ARP(prazoRestante, dataFinal, hoje):
    mensagem = " "
    if dataFinal >= hoje:
        mensagem = f"O contrato é válido por mais {prazoRestante.years} anos, {prazoRestante.months} meses e {prazoRestante.days} dias."
        return mensagem
    else:
        mensagem =  "O prazo de validade do contrato já expirou."
    return mensagem


# INDEX
@login_required
def index(request):
    return render(request, 'index.html')

#cadastro de fornecedor
def fornecedor_new(request):
    if request.method=='POST':
        form = formFornecedor(request.POST)
        if form.is_valid():
            fornecedor=form.save() 
            print(f"id do fornecedor = {fornecedor.id}")
            #redirecionar de volta para a tela de cadastro fornecendo o ID do fornecedor 
            return redirect('biddingContracts:cadContrato', fornecedor_id = fornecedor.id)
        else:
            print('ocorreu um erro no fomulario', form.errors)
    else:
        form = formFornecedor()
        return render(request, 'fornecedor_new.html', {'form': form})
    
def listFornecedores(request):
    fornecedores = Fornecedor.objects.all()
    context = {"fornecedores": fornecedores}
    return render(request, "fornecedores.html", context)

def modal_fornecedor(request):
    "mostra fornecedor em um modal"
    fornecedores = Fornecedor.objects.all()
    context = {"fornecedores": fornecedores}
    return render(request, "modal_fornecedores.html", context)

def listLicitacoes(request):
    """mostra todas as licitacoes"""
    licitacoes = Licitacao.objects.all()
    context = {"licitacoes": licitacoes}
    return render(request, "list_licitacoes.html", context)
#MODAL
"""def modal_licitacao(request):
    "mostra licitacao em um modal"
    licitacoes = Licitacao.objects.all()
    context = {"licitacoes": licitacoes}
    return render(request, "modal_bidding.html", context)
"""
class BiddingCreateView(CreateView):
    """
    Faz o cadastro das licitações
    """
    model = Licitacao
    form_class = formLicitacao
    template_name = 'licitacoes.html'
    message_success = 'Licitação criada com sucesso!'
    #success_url = reverse_lazy

    def get_success_url(self) -> str:
        messages.success(self.request, self.message_success)
        return reverse_lazy('biddingContracts:list_bidding')


class ListBiddingView(ListView):
    """
    Faz a listagem das licitações
    """
    model = Licitacao
    template_name = "list_licitacoes.html"
    context_object_name = "licitacoes"

    def get_queryset(self):
        txt_buscar = self.request.GET.get("buscar")
        queryset = Licitacao.objects.all()
        if txt_buscar:
            queryset = queryset.filter(
                Q(categoria__icontains=txt_buscar) |
                Q(assunto__icontains=txt_buscar) |
                Q(numProcess__icontains=txt_buscar)
            )
        return queryset
    


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

 
"""class BiddingCreateArp(CreateView):
    model=AtaRegistroPreco
    form_class = formARP
    template_name = 'ataRegistroPreco_new.html'
    success_url = reverse_lazy('biddingContracts:create-ARP')"""


def createArp(request):
    if request.method == "POST":
        form = formARP(request.POST)
        print("enviando método POST")
        if form.is_valid(): #por que o formulário não está sendo validaddo?
            arp = form.save(commit=False)
            dataInicial = arp.dataInicial
            print("formulario valido", dataInicial)
            if dataInicial:
                dataFinal = dataInicial + relativedelta(days=365)
                arp.dataFinal = dataFinal
                print("dataInicial Validada", arp.dataFinal)
            arp.save()
            return HttpResponseRedirect(reverse('biddingContracts:atas'))
    else:
        form = formARP()
    context = {'form': form}
    return render(request, "ataRegistroPreco_new.html", context)

class listARPs(ListView):
    model=AtaRegistroPreco
    template_name='atas.html'
    success_url= reverse_lazy('biddingContracts:atas')

 
 # View que atualiza as licitações
class BiddingUpdateView(UpdateView):
    model = Licitacao
    template_name = "licitacoes/edit_licitacoes.html"
    form_class = formLicitacao
    context_object_name = "licitacao"

    def form_valid(self, form):
        messages.success(self.request, 'Licitação editada com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao editar licitação. Verifique os campos do formulário.')
        return render(self.request, self.template_name, {"form": form})

    def get_success_url(self):
        return reverse_lazy("biddingContracts:licitacoes")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class FornecedorUpdate(UpdateView):
    model=Fornecedor
    template_name = "fornecedor_update.html"
    form_class = formFornecedor
    context_object_name = "fornecedor"


    def form_valid(self, form):
        messages.success(self.request, 'fornecedor editado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao editar fornecedor. Verifique os campos do formulário.')
        return render(self.request, self.template_name, {"form": form})

    def get_success_url(self):
        return reverse_lazy("biddingContracts:fornecedores")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
#view para salvar as licitações como pdf
def export_pdf(request): 
    biddings = Licitacao.objects.all() # lista todas as licitações 
    html_index = render_to_string('pdf/export-pdf.html', {'licitacoes': biddings})  
    weasyprint_html = weasyprint.HTML(string=html_index, base_url='http://127.0.0.1:8000/media')
    pdf = weasyprint_html.write_pdf(stylesheets=[weasyprint.CSS(string='body { font-family: serif} img {margin: 10px; width: 50px;}')]) 
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Products'+str(date.today())+'.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(pdf)
        output.flush() 
        output.seek(0)
        response.write(output.read()) 
    return response

class NotasFiscaisView(CreateView):
    model= NotaFiscal
    form_class = NotaFiscalForm
    template_name = "notaFiscal_new.html"
    print("notas fiscais view")
    success_url = reverse_lazy("biddingContracts:notasfiscais")

class ListNfe(ListView):
    model = NotaFiscal
    template_name = "notasFiscais.html"
    success_url = reverse_lazy("biddingContracts:notasfiscais")