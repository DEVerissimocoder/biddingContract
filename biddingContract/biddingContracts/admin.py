from django.contrib import admin
from .models import Licitacao, Contrato, Fornecedor
# Register your models here.
admin.site.register(Licitacao)
admin.site.register(Contrato)
admin.site.register(Fornecedor)
