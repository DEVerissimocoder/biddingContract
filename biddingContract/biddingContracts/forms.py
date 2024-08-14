from django import forms
from .models import Licitacao, Fornecedor, Contrato

class formLicitacao(forms.ModelForm):
    class Meta:
        model = Licitacao
        fields = [
            "numProcess",
            "categoria",
            "assunto",
            "date",
        ]

        labels = {
            "numProcess": "Número do Processo",
            "categoria": "Categoria",
            "assunto": "Detalhe da Licitação",
            "date": "Data de criação"
        }

        widgets = {
            "numProcess": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "placeholder": "Número da licitação"
                }
            ),
            "categoria": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "placeholder": "Categoria"
                }
            ),
            "assunto": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Descreva de que se trata a licitação"
                }
            ),
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),
        }


class formFornecedor(forms.ModelForm):
    class Meta: 
        model = Fornecedor
        fields = "__all__"


class formContrato(forms.ModelForm):
    licitacao_fk = forms.ModelChoiceField(
        queryset=Licitacao.objects.all(),
        label="Licitação",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    fornecedor_fk = forms.ModelChoiceField(
        queryset=Fornecedor.objects.all(),
        label="Fornecedor",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Contrato
        fields = [
            "numero",
            "assuntoDetalhado",
            "dataInicial",
            "dataFinal",
            "valor",
            "licitacao_fk",
            "fornecedor_fk",
        ]
        labels = {
            "numero": "Número do Processo",
            "assuntoDetalhado": "Detalhe do contrato",
            "dataInicial": "Início do Contrato",
            "dataFinal": "Término do Contrato",
            "valor": "Valor do Contrato",
            "licitacao_fk": "Licitação",
            "fornecedor_fk": "Fornecedor"
        }
        widgets = {
            "numero": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "placeholder": "Número do Contrato"
                }
            ),
            "assuntoDetalhado": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Descreva de que se trata o contrato",
                    "rows": 3,  # Adicionando rows para controle da altura do campo
                }
            ),
            "dataInicial": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),
            "dataFinal": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),
            "valor": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Valor do Contrato",
                }
            ),
        }
