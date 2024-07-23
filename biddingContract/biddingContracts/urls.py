from . import views
from django.urls import path

urlpatterns = [
    path('contratos/', views.listContratos, name="contratos"),
    path('contratos/relatorio/<id_contrato>', views.contratosRelatorio, name='relatorio')
]
