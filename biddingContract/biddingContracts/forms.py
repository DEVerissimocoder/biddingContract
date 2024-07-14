from django import forms
from .models import Licitacao

class formLicitacao(forms.ModelForm):
    class Meta:
        model = Licitacao
        fields = "__all__"
