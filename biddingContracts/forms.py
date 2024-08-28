from django import forms
from .models import Licitacao, Fornecedor, Contrato, AtaRegistroPreco

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
            "numProcess": "PROCESSO",
            "categoria": "MODALIDADE",
            "assunto": "OBJETO",
            "date": "DATA"
        }

        widgets = {
            "numProcess": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "placeholder": "Número da licitação",
                    "id": "proc",
                }
            ),
            "categoria": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "placeholder": "Modalidade"
                }
            ),
            "assunto": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "ex.: material de expediente"
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
        fields=[
        "nome",
        "cnpj",
        "endereco",
        "num",
        "bairro",  
        "cep",
        "cidade", 
        "telefone"
        ]

        labels={
            "nome": "Razão Social",
        }

        widgets = {
            "nome": forms.TextInput(
                attrs={
                "type": "text",
                "class": "form-control", 
                "placeholder": "razão social",
                
                }
            ),  
        }

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
            "numero": "NÚMERO",
            "assuntoDetalhado": "OBJETO DETALHADO",
            "dataInicial": "DATA INICIAL",
            "dataFinal": "DATA FINAL",
            "valor": "VALOR",
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

class formARP(forms.ModelForm):
    licitacao_fk = forms.ModelChoiceField(
        queryset=Licitacao.objects.all(),
        label="Licitação",
        #widget=forms.Select(attrs={'class': 'form-select'})
    )

    fornecedor_fk = forms.ModelChoiceField(
        queryset=Fornecedor.objects.all(),
        label="Fornecedor",
        #widget=forms.Select(attrs={'class': 'form-select'})
    )
    data= forms.DateField()
    dataFinal = forms.DateField()
    
    class Meta:
        model = AtaRegistroPreco
        fields = [
            "numero",
            "assuntoDetalhado",
            "data",
            "dataFinal",
            "valor",
            "licitacao_fk",
            "fornecedor_fk",
        ]
        labels = {
            "numero": "NÚMERO",
            "assuntoDetalhado": "OBJETO DETALHADO",
            "data": "DATA INICIAL",
            "dataFinal": "data Final",
            "valor": "VALOR",
            "licitacao_fk": "Licitação",
            "fornecedor_fk": "Fornecedor"
        }
        widgets = {
            "numero": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "placeholder": "Número Ata de Registro de Preços"
                }
            ),
            "assuntoDetalhado": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Descreva o objeto relacionado a Ata de Registro de Preços (ARP)",
                    "rows": 2,  # Adicionando rows para controle da altura do campo
                }
            ),
            "data": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),
            "dataFinal": forms.HiddenInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),
            "valor": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Valor da Ata de Registro de Preços",
                }
            ),
        }
