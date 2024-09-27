from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
from django.db.models import Q
from  biddingContracts.forms import formLicitacao, formFornecedor,NotaFiscalEditForm, formContrato, formARP, NotaFiscalForm
from django.urls import reverse, reverse_lazy
from .models import Contrato, NotaFiscal, Fornecedor, Licitacao, AtaRegistroPreco
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages

import tempfile
from django.utils import timezone
#import weasyprint
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required


# CONTRATOS + RELATORIOS
# def cadContrato(request):
#     if request.method == "POST":
#         form = formContrato(request.POST)
#         print("post")
#         if form.is_valid():
#             print("formulario validado")
#             form.save()
#             return HttpResponseRedirect(reverse("biddingContracts:contratos"))
#         else:
#             print(f"Deu errado!{form.errors}")
#     else:
#         form = formContrato()
        

#     return render(request, "contrato_new.html", {"form": form})
"""def teste(request):
    return render(request, "modal_fornecedor_teste.html")"""

@login_required
def cadContrato(request, fornecedor_id):
    if request.method == "POST":
        form = formContrato(request.POST)
        print(f"Dados recebidos no POST: {request.POST}") 
        if form.is_valid():
            form.save()
            messages.success(request, "Cadastro criado com sucesso!")
            return HttpResponseRedirect(reverse("biddingContracts:contratos"))
        else:
            print(f"Deu errado!{form.errors}")
    else:
        form = formContrato()

    return render(request, "contratos/contrato_new.html", {"form": form, "fornecedor_id": fornecedor_id})
    

# def listContratos(request):
#     contratos = Contrato.objects.all()
#     context = {"contratos": contratos}
#     print("chamando view")
#     return render(request, "contratos.html", context)

# class ListContractsView(LoginRequiredMixin, ListView):
    
#     # fluxo 2-> segunda requisição, ou seja, quando ele vem da tela de cadastro de fornecedor.
#     if fornecedor_id!=0:
#         #consulta o fornecedor vindo do banco através do ID e cria um objeto com os dados retornado da tabela fornecedor
#         fornecedor = Fornecedor.objects.get(id = fornecedor_id)
        
#         form = formContrato()
#         context={'form':form, 'fornecedor_id':fornecedor.id}
#         return render(request, 'contrato_new.html', context)
    
#     # fluxo 1 -> primeira requisição get
#     else:
#         form = formContrato()
#         context={'form':form,'fornecedor_id':fornecedor_id}
#         return render(request, "contrato_new.html", context)
    
class ListContractsView(ListView):
    """
    Classe destinada a listar os contratos criados
    """
    model = Contrato
    template_name = "contratos/contratos.html"
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
    
     # Adicionando o cálculo de vencimento ao contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contratos = context['contratos']
        today = timezone.now().date()  # Obtém a data atual

        # Adiciona um atributo 'vencido' a cada contrato
        for contrato in contratos:
            contrato.vencido = today > contrato.dataFinal  # Verifica se o contrato já venceu

        return context

# View que atualiza os contratos
class ContractsUpdateView(LoginRequiredMixin, UpdateView):
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
        context['fornecedores'] = Fornecedor.objects.all()
        return context

@login_required
def contratosRelatorio(request, id_contrato):
    contrato = Contrato.objects.get(id=id_contrato)
    notasFiscais = NotaFiscal.objects.filter(contrato_fk = id_contrato)
    saldoAtual = contrato.valor
    #tipo datetime.date
    hoje = datetime.today().date()
    
    # tipo datetime.date
    dataFinalContrato = contrato.dataFinal  
    print(f'data final= {type(hoje)}')
    prazoRestante = relativedelta(dataFinalContrato, hoje)
    
    mensagem = verifica_prazo_validade(prazoRestante, dataFinalContrato, hoje)

    for notas in notasFiscais:
        if notas.contrato_fk.numero == contrato.numero:
            saldoAtual -= notas.valor
    context = {
        "notasfiscais": notasFiscais,
        "saldoAtual": saldoAtual,
        "vigencia": mensagem,
        "hoje": hoje,
        "dataFinal": dataFinalContrato,
        "chave":True
        }
    return render(request, "contratos/contratos_relatorio.html", context)



def verifica_prazo_validade(prazoRestante, dataFinal,  hoje):
    mensagem = ""
    if dataFinal > hoje:
        mensagem = f"O contrato é válido por mais {prazoRestante.years} anos, {prazoRestante.months} meses e {prazoRestante.days} dias."
        return mensagem
    elif dataFinal == hoje:
        mensagem = f"O contrato é válido até hoje dia: {dataFinal.strftime('%d/%m/%y')}"
        return mensagem
    elif dataFinal < hoje:
        mensagem =  f"O prazo de validade do contrato já expirou."
    return mensagem

def verifica_prazo_validade_arp(prazoRestante, dataFinal, hoje):
    # return verifica_prazo_validade(prazoRestante, dataFinal, hoje, tipo="ARP")
    mensagem = ""
    if dataFinal > hoje:
        mensagem = f"Esta ARP é válida por mais {prazoRestante.years} anos, {prazoRestante.months} meses e {prazoRestante.days} dias."
        return mensagem
    elif dataFinal == hoje:
        mensagem = f"Esta ARP é válido até hoje dia: {dataFinal.strftime('%d/%m/%y')}"
        return mensagem
    elif dataFinal < hoje:
        #Aqui eu vi uma utilidade de ser armazenado no banco de dados o valor atual da ARP para quando 
        # for cadastrar o contrato já inserir o valor automaticamente para evitar possíveis erros do 
        # usuário de digitar um valor diferente do valor atual do contrato.
        mensagem =  "O prazo de validade desta ARP expirou, cadastre-a como contrato usando o saldo atual, clique aqui:" 
        
    return mensagem


# INDEX
@login_required
def index(request):
    if request.user.is_authenticated:
        nome_usuario = request.user.username.title()
        aviso = f"Olá, {nome_usuario }. Seja bem-vindo!"
        messages.success(request, aviso)
    return render(request, 'index.html')


# View que Cria os fornecedores
class BiddingFornecedor(LoginRequiredMixin, CreateView):
    model = Fornecedor
    form_class = formFornecedor
    template_name = 'fornecedor/fornecedor_new.html'
    success_url = reverse_lazy('biddingContracts:cadContrato')
def fornecedor_new(request):
    if request.method=='POST':
        form = formFornecedor(request.POST)
        if form.is_valid():
            fornecedor=form.save() 
            print(f"id do fornecedor = {fornecedor.id}")
            #redirecionar de volta para a tela de cadastro fornecendo o ID do fornecedor
            # aqui terá 2 fluxos: 1 redirecionar para a página de contrato e outro para ARP 
            messages.success(request, "Fornecedor cadastrado com sucesso!")
            return redirect('biddingContracts:cadContrato', fornecedor_id = fornecedor.id)
        else:
            print('ocorreu um erro no fomulario', form.errors)
    else:
        form = formFornecedor()
        return render(request, 'fornecedor/fornecedor_new.html', {'form': form})


@login_required
# View que lista os fornecedores
def listFornecedores(request):
    fornecedores = Fornecedor.objects.all()
    context = {"fornecedores": fornecedores}
    return render(request, "fornecedor/fornecedores.html", context)


@login_required
# View que mostra fornecedor em um modal
def modal_fornecedor(request):
    "mostra fornecedor em um modal"
    fornecedores = Fornecedor.objects.all()
    context = {"fornecedores": fornecedores}
    return render(request, "fornecedor/modal_fornecedores.html", context)


@login_required
# View que lista as Licitações
def listLicitacoes(request):
    """mostra todas as licitacoes"""
    licitacoes = Licitacao.objects.all()
    context = {"licitacoes": licitacoes}
    return render(request, "licitacoes/list_licitacoes.html", context)


@login_required
# View que mostra a licitação em um modal
def modal_licitacao(request):
    "mostra licitacao em um modal"
    licitacoes = Licitacao.objects.all()
    context = {"licitacoes": licitacoes}
    return render(request, "licitacao/modal_bidding.html", context)


# View que faz o cadastro das licitações
class BiddingCreateView(LoginRequiredMixin, CreateView):
    """
    Faz o cadastro das licitações
    """
    model = Licitacao
    form_class = formLicitacao
    template_name = 'licitacoes/licitacoes.html'
    message_success = 'Licitação criada com sucesso!'
    #success_url = reverse_lazy

    def get_success_url(self) -> str:
        messages.success(self.request, self.message_success)
        return reverse_lazy('biddingContracts:list_bidding')


# View que faz a listagem das licitações com a pesquisa 
class ListBiddingView(LoginRequiredMixin, ListView):
    """
    Faz a listagem das licitações
    """
    model = Licitacao
    template_name = "licitacoes/list_licitacoes.html"
    context_object_name = "licitacoes"

    # Adicionando filtros ao object_list através do get_queryset
    def get_queryset(self):
        txt_licitacao = self.request.GET.get("licitacao")
        txt_assunto = self.request.GET.get("assunto")
        txt_datas = self.request.GET.get("datas")
        txt_categorias = self.request.GET.get("categorias")
        

        if txt_licitacao:
            queryset = Licitacao.objects.filter(numProcess__icontains=txt_licitacao)
            return queryset
        
        elif txt_categorias:
            queryset = Licitacao.objects.filter(categoria__icontains=txt_categorias)
            return queryset
        
        elif txt_datas:
            try:
                data_formatada = datetime.strptime(txt_datas, '%d/%m/%Y').date()
                queryset = Licitacao.objects.filter(date=data_formatada)
                return queryset
            except ValueError:
                messages.error(self.request, 'Data inválida! Por favor, insira uma data no formato dd/mm/yyyy.')
                return redirect('biddingContracts:licitacoes')
        
        elif txt_assunto:
            queryset = Licitacao.objects.filter(assunto__icontains=txt_assunto)
            return queryset
            
        txt_buscar = self.request.GET.get("buscar")
        queryset = Licitacao.objects.all()
        if txt_buscar:
            queryset = queryset.filter(
                Q(categoria__icontains=txt_buscar) |
                Q(assunto__icontains=txt_buscar) |
                Q(numProcess__icontains=txt_buscar)
            )
        else:
            queryset = Licitacao.objects.all()
        return queryset


@login_required
# Função que cria as ARPs
def createArp(request):
    if request.method == "POST":
        form = formARP(request.POST)
        print("enviando método POST")
        if form.is_valid():
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
    return render(request, "ARPs/ataRegistroPreco_new.html", context)


# View que lista as ARPs
class listARPs(LoginRequiredMixin, ListView):
    model=AtaRegistroPreco
    template_name='ARPs/atas.html'
    success_url= reverse_lazy('biddingContracts:atas')
    context_object_name = "atas"


# View que edita ARPs
class ARPsUpdate(LoginRequiredMixin, UpdateView):
    model=AtaRegistroPreco
    template_name = "ARPs/ata_update.html"
    form_class = formARP
    context_object_name = "ata"


    def form_valid(self, form):
        messages.success(self.request, 'ARP editada com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao editar ARP. Verifique os campos do formulário.')
        return render(self.request, self.template_name, {"form": form})

    def get_success_url(self):
        return reverse_lazy("biddingContracts:atas")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# View que deleta as ARPs
class ARPsDeleteView(LoginRequiredMixin, DeleteView):
    model = AtaRegistroPreco
    template_name = "ARPs/ata_delete.html"
    context_object_name = "ata"

    def get_success_url(self):
        messages.success(self.request, 'ARP excluída com sucesso!')
        return reverse_lazy("biddingContracts:atas")
 
 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['atas'] = AtaRegistroPreco.objects.all()
        return context


class RelatorioARPs(ListView):
    model = AtaRegistroPreco
    template_name = 'contratos/contratos_relatorio.html'
   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ata_id = self.kwargs.get('pk')  #captura a ata pelo id na url
        notasfiscais = NotaFiscal.objects.filter(ataregistropreco_fk_id = ata_id)
        ata = AtaRegistroPreco.objects.get(id=ata_id) # captura o objeto inteiro

        hoje = datetime.today()
        hoje = hoje.date()
        dataInicial = ata.dataInicial
        dataFinal = ata.dataFinal
        # calculo de quanto tempo falta para o fim da ARP
        prazoRestante = relativedelta(dataFinal,hoje)
        print(hoje)
        #mensagem que será levada para o template
        mensagem=verifica_prazo_validade_arp(prazoRestante, dataFinal, hoje)
        #saldo restante da ARP
        saldoAtual = calcula_saldo_restante(notasfiscais, ata.valor)

        context["vigencia"] = mensagem
        context["hoje"]=hoje
        context["dataFinal"] = dataFinal
        context["prazoRestante"] = prazoRestante
        context["notasfiscais"] = notasfiscais
        context['saldoAtual']=saldoAtual
        context["chave"] = False
        return context

def calcula_saldo_restante(notasfiscais, valorARP):
    soma=0
    for nota in notasfiscais:
        soma+=nota.valor  
    return valorARP - soma
    
 # View que atualiza as licitações
class BiddingUpdateView(LoginRequiredMixin, UpdateView):
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



# View que edita os fornecedores
class FornecedorUpdate(LoginRequiredMixin, UpdateView):
    model=Fornecedor
    template_name = "fornecedor/fornecedor_update.html"
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
    

# #view para salvar as licitações como pdf
# def export_pdf(request): 
#     biddings = Licitacao.objects.all() # lista todas as licitações 
#     html_index = render_to_string('pdf/export-pdf.html', {'licitacoes': biddings})  
#     weasyprint_html = weasyprint.HTML(string=html_index, base_url='http://127.0.0.1:8000/media')
#     pdf = weasyprint_html.write_pdf(stylesheets=[weasyprint.CSS(string='body { font-family: serif} img {margin: 10px; width: 50px;}')]) 
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename=Products'+str(date.today())+'.pdf'
#     response['Content-Transfer-Encoding'] = 'binary'
#     with tempfile.NamedTemporaryFile(delete=True) as output:
#         output.write(pdf)
#         output.flush() 
#         output.seek(0)
#         response.write(output.read()) 
#     return response


# # View que cria as notas fiscais
# class NotasFiscaisView(LoginRequiredMixin, CreateView):
#     model= NotaFiscal
#     form_class = NotaFiscalForm
#     template_name = "notaFiscal_new.html"
#     print("notas fiscais view")
#     success_url = reverse_lazy("biddingContracts:notasfiscais")
def notafiscal_new(request):
    #requisição post
    if request.method=='POST':
        hoje = datetime.today()
        dhoje= hoje.date()
        form = NotaFiscalForm(request.POST)
        
        if form.is_valid():
            print("formulario valido")
            if form.cleaned_data['contrato_fk']:
                print("nota fiscal - contrato")
                contrato = Contrato.objects.get(numero=form.cleaned_data['contrato_fk'])
                #pega do banco todas as notas fiscais relacionado ao contrato em questão
                notasfiscais = NotaFiscal.objects.filter(contrato_fk_id = contrato.id)
                #soma os valores das notas fiscais do contrato, que já estão armazenadas no banco, mais a nota que está tentando cadastrar
                soma = sum(nota.valor for nota in notasfiscais) + form.cleaned_data.get('valor')
            
                # valida se o resultado da soma ultrapassa o valor total do contrato.
                if soma > contrato.valor:
                    messages.add_message(request, messages.INFO, "NÃO FOI POSSÍVEL CADASTRAR A NOTA FISCAL, VALOR DA NOTA MAIOR DO QUE O SALDO RESTANTO DO CONTRATO")
                    return HttpResponseRedirect(reverse('biddingContracts:nfe'))
                #verificação da data de vigência
                if contrato.dataFinal<dhoje:
                    messages.add_message(request, messages.INFO, "NÃO FOI POSSIVEL CADASTRAR NOTAS, CONSULTE O VALOR RESTANTE DO CONTRATO")
                    return HttpResponseRedirect(reverse("biddingContracts:nfe"))
            else: 
                print("notafiscal - ata de registro de preços")
                arp = AtaRegistroPreco.objects.get(numero=form.cleaned_data['ataregistropreco_fk'])
                #pega do banco todas as notas fiscais relacionado a ARP em questão
                
                notasfiscais = NotaFiscal.objects.filter(ataregistropreco_fk_id = arp.id)
                soma = sum(nota.valor for nota in notasfiscais) + form.cleaned_data.get('valor')
            
                # valida se o resultado da soma ultrapassa o valor total da ARP
                if soma > arp.valor:
                    messages.add_message(request, messages.INFO, "NÃO FOI POSSÍVEL CADASTRAR A NOTA FISCAL, VALOR DA NOTA MAIOR DO QUE O SALDO RESTANTE DA ATA DE REGISTRO DE PREÇOS")
                    return HttpResponseRedirect(reverse('biddingContracts:nfe'))
                #verificação da data de vigência
                if arp.dataFinal<dhoje:
                    messages.add_message(request, messages.INFO, "NÃO FOI POSSIVEL CADASTRAR NOTAS, CONSULTE O VALOR RESTANTE DA ATA DE REGISTRO DE PREÇO")
                    return HttpResponseRedirect(reverse("biddingContracts:nfe"))
            form.save()
            messages.add_message(request, messages.SUCCESS, "SALVO COM SUCESSO")
            return HttpResponseRedirect(reverse('biddingContracts:notasfiscais'))
        else:
            print(form.errors)
    #requisição get.
    print("formulario vazio")
    form = NotaFiscalForm()
    return render(request, 'notafiscal/notaFiscal_new.html', {"form":form})


# View que lista as Notas Fiscais
class ListNfe(LoginRequiredMixin, ListView):
    model = NotaFiscal
    template_name = "notafiscal/notasFiscais.html"
    success_url = reverse_lazy("biddingContracts:notasfiscais")


# View que edita as Notas fiscais
class NotasFiscaisUpdate(LoginRequiredMixin, UpdateView):
    model=NotaFiscal
    template_name = "notafiscal/notafiscal_update.html"
    form_class = NotaFiscalEditForm
    context_object_name = "notas"


    def form_valid(self, form):
        messages.success(self.request, 'Nota Fiscal editada com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao editar nota fiscal . Verifique os campos do formulário.')
        return render(self.request, self.template_name, {"form": form})

    def get_success_url(self):
        return reverse_lazy("biddingContracts:notasfiscais")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
# View que deleta as Notas fiscais
class NotesDeleteView(LoginRequiredMixin, DeleteView):
    model = NotaFiscal
    template_name = "notafiscal/nota_delete.html"
    context_object_name = "note"

    def get_success_url(self):
        messages.success(self.request, 'Nota Fiscal excluída com sucesso!')
        return reverse_lazy("biddingContracts:notasfiscais")
    