from django import forms
from .models import Licitacao, Fornecedor, Contrato

class formLicitacao(forms.ModelForm):
    class Meta:
        model = Licitacao
        fields = "__all__"


class formFornecedor(forms.ModelForm):
    class Meta: 
        model = Fornecedor
        fields = "__all__"

class formContrato(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = "__all__"