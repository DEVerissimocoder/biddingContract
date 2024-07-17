from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('cad_licitacao/', views.cadLicitacao, name='cadLicitacao'),
    path('licitacoes/', views.listLicitacoes, name='listLicitacoes'),   
    path('fornecedor_new/', views.cadFornecedor, name='fornecedor_new'  ),
    path('fornecedores/', views.listFornecedores, name="listFornecedores")
    
]
