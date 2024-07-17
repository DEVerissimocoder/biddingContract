from django import forms
from .models import Licitacao, Fornecedor

class formLicitacao(forms.ModelForm):
    class Meta:
        model = Licitacao
        fields = "__all__"


class formFornecedor(forms.ModelForm):
    class Meta: 
        model = Fornecedor
        fields = "__all__"
