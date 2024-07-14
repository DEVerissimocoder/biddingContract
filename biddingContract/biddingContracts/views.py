from django.shortcuts import render
from django.http import HttpResponseRedirect
from  .forms import formLicitacao
from django.urls import reverse
from .models import Licitacao
# Create your views here.



def cadLicitacao(request):
    if (request.method == 'POST'):
        form = formLicitacao(request.POST)
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('listLicitacoes'))
    else:
        form = formLicitacao()
    return render(request, 'biddingContracts/cad_licitacao.html', {"form": form})

def listLicitacoes(request):
    """mostra todas as licitacoes"""
    licitacoes = Licitacao.objects.all()
    context = {"licitacoes": licitacoes}
   
    return render(request, "biddingContracts/licitacoes.html", context)
   

def index(request):
    return render(request, 'biddingContracts/index.html')