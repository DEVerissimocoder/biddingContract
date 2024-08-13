from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('contratos/', views.listContratos, name="contratos"),
    path('contratos/relatorio/<id_contrato>', views.contratosRelatorio, name='relatorio'),
    path('fornecedores/', views.listFornecedores, name="fornecedores"),
    path('licitacoes/', views.listLicitacoes, name='licitacoes'),
    path('contrato/', views.cadContrato, name="cadContrato")
]
