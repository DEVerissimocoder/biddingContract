from . import views
from django.urls import path

app_name = 'biddingContracts'

urlpatterns = [
    path('', views.index, name='index'),
    #path('contratos/', views.listContratos, name="contratos"),
    path("contratos/", views.ListContractsView.as_view(), name="contratos"),
    path('contratos/relatorio/<int:id_contrato>', views.contratosRelatorio, name='relatorio'),
    path('contratos/<int:pk>/editar/', views.ContractsUpdateView.as_view(), name='update_contracts'),
    #path('contratos/<int:id_contrato>/relatorio/', views.ContratoRelatorioView.as_view(), name='contrato_relatorio'),
    path('fornecedores/', views.listFornecedores, name="fornecedores"),
    path('criar-fornecedor/', views.fornecedor_new, name='fornecedor_new'),
    path('licitacoes/', views.ListBiddingView.as_view(), name="list_bidding"),
    path('updt-fornecedor/<int:pk>/', views.FornecedorUpdate.as_view(), name='updateforn'),
    path('modal-fornecedor/', views.modal_fornecedor, name="modal-fornecedor"),
    path('licitacoes/', views.listLicitacoes, name='licitacoes'),
    path('criar-licitacoes/', views.BiddingCreateView.as_view(), name='create-bidding'),
    path('modal-licitacao/', views.modal_licitacao, name='modal-licitacao'),
    path('contrato/<int:fornecedor_id>', views.cadContrato, name="cadContrato"),
    #path('export-pdf/', views.export_pdf, name='export-pdf'),
    path('licitacoes/<int:pk>/editar/', views.BiddingUpdateView.as_view(), name='update_bidding'),
    path('criar-ARP/', views.createArp, name='create-ARP'),#ARP - SIGLA PARA (ATA DE REGISTRO DE PREÇOS)
    path('atas/', views.listARPs.as_view(), name="atas"), #Listar ARPs
    path('relatorio-atas/<int:pk>', views.RelatorioARPs.as_view(), name='relatorioARP'),
    path('atas-edit/<int:pk>/', views.ARPsUpdate.as_view(), name="updateARP"), #Editar ARPS
    path('atas-delete/<int:pk>/', views.ARPsDeleteView.as_view(), name="deleteARP"), #Deletar ARPS
    path('criar-notafiscal/', views.NotasFiscaisView.as_view(), name='nfe'),
    path('notasfiscais/', views.ListNfe.as_view(), name='notasfiscais'), #Listar Notas Fiscais
    path('editarnfe/<int:pk>/', views.NotasFiscaisUpdate.as_view(), name='updatenfe'), #Editar Notas Fiscais
    path('deletenfe/<int:pk>/', views.NotesDeleteView.as_view(), name='deletenfe'),
    path('atas/', views.listARPs.as_view(), name="atas"),
    
    #path('teste/', views.teste, name='teste')
]
