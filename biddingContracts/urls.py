from . import views
from django.urls import path

app_name = 'biddingContracts'

urlpatterns = [
    path('', views.index, name='index'),
    path('contratos/', views.listContratos, name="contratos"),
    path('contratos/relatorio/<int:id_contrato>', views.contratosRelatorio, name='relatorio'),
    path('fornecedores/', views.listFornecedores, name="fornecedores"),
    path('criar-fornecedor/', views.BiddingFornecedor.as_view(), name='fornecedor_new'),
    path('licitacoes/', views.listLicitacoes, name='licitacoes'),
    path('criar-licitacoes/', views.BiddingCreateView.as_view(), name='create-bidding'),
    path('contrato/', views.cadContrato, name="cadContrato"),
    path('buscar/', views.BuscarView.as_view(), name='buscar'),
    path('export-pdf/', views.export_pdf, name='export-pdf'),
    path('licitacoes/<int:pk>/editar/', views.BiddingUpdateView.as_view(), name='update_bidding'),
    path('criar-ARP/', views.createArp, name='create-ARP'),#ARP - SIGLA PARA (ATA DE REGISTRO DE PREÇOS)
    path('atas/', views.listARPs.as_view(), name="atas")
]
