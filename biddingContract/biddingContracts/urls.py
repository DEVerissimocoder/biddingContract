from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('cad_licitacao/', views.cadLicitacao, name='cadLicitacao'),
    path('licitacoes/', views.listLicitacoes, name='ListLicitacoes')    
    
]
