from django import forms
from .models import Licitacao, Fornecedor, Contrato, AtaRegistroPreco, NotaFiscal

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
                    "placeholder": "ex.: material de expediente",
                    "rows":2,
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
                "required": True,
                }
            ),
            "cnpj": forms.TextInput(
                attrs={
                "type": "text",
                "class": "form-control", 
                "placeholder": "Apenas números",
                "required": True,
                "id": "cnpj",
                }
            ),
            "endereco": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "placeholder": "Endereço",
                    "required": True,
                }
            ),
            "num": forms.NumberInput(
                attrs={
                    "type": "number",
                    "class": "form-control",
                    "placeholder": "Número",
                    "required": True,
                }
            ),
            "bairro": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "placeholder": "Bairro",
                    "required": True,
                }
            ),
            "cep": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "placeholder": "ex: 00000-000",
                    "required": True,
                    "id": "cep",
                }
            ),
            "cidade": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "placeholder": "Cidade",
                    "required": True,
                }
            ),
            "telefone": forms.NumberInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "placeholder": "Telefone",
                    "required": True,
                    "id": "phone",
                }
            )
        }   

class formContrato(forms.ModelForm):
    
    # licitacao_fk = forms.ModelChoiceField(
    #     queryset=Licitacao.objects.all(),
    #     label="Licitação",
    #     widget=forms.Select(attrs={'class': 'form-select'})
    # )
  
    """fornecedor_fk = forms.ModelChoiceField(
        queryset=Fornecedor.objects.all(),
        label="Fornecedor",
        widget=forms.Select(attrs={'class': 'form-select'})
    )"""

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
            "licitacao_fk": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "placeholder": "licitacoes ao lado",
                }
            ),
            "fornecedor_fk": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "placeholder": "fornecedor",
                }
            ),

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
                    "type": "number",
                    "class": "form-control",
                    "placeholder": "Valor do Contrato",
                    "id": "money",
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
    
    class Meta:
        model = AtaRegistroPreco
        fields = [
            "numero",
            "assuntoDetalhado",
            "dataInicial",
            "valor",
            "licitacao_fk",
            "fornecedor_fk",
        ]
        labels = {
            "numero": "NÚMERO",
            "assuntoDetalhado": "OBJETO DETALHADO",
            "dataInicial": "DATA INICIAL",
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
            "dataInicial": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),
            "valor": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Valor da Ata de Registro de Preços",
                }
            ),
        }

class NotaFiscalForm(forms.ModelForm):
    class Meta:
        model = NotaFiscal
        fields=["num", "serie", "valor", "tipo", "dataEmissao", "contrato_fk"]
        labels={
                "num": "NÚMERO",
                "serie": "SERIE",
                "valor": "VALOR",
                "tipo": "TIPO", #acho que este campo poderia sair, já que que tem o campo serie.
                "dataEmissao": "DATA DE EMISSÃO",
                "contrato_fk": "CONTRATO"
                }
        
        widgets={
            "num":forms.NumberInput(
                attrs={
                    "type":"number",
                    "class":"form-control",
                }
            ),
            "serie": forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "form-control"
                }
            ),
            "valor": forms.NumberInput(
                attrs={
                    "type":"number",
                    "class": "form-control",
                }
            ),
            "tipo": forms.TextInput(
                attrs={
                    "type":"text",
                    "class": "form-control",
                }
            ),
            "dataEmissao": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),
            

        }
            
