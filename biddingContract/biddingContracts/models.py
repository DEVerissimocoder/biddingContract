from django.db import models

#licitacao
class Licitacao (models.Model):
    numProcess = models.IntegerField(primary_key=True)
    categoria = models.CharField(max_length=200, null=False)
    assunto = models.CharField(max_length=200)
    date = models.DateField()

    class meta:
        verbose_name_plural = "licitações"

#Fornecedor
class Fornecedor(models.Model):
    nome = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=200)
    endereco = models.CharField(max_length=200)
    num  = models.CharField(max_length=200)
    bairro  = models.CharField(max_length=200)
    cep = models.CharField(max_length=200)
    telefone = models.CharField(max_length=200)

    class meta:
        verbose_name_plural = "fornecedores"

#Contrato
class Contrato(models.Model):
    numero = models.IntegerField(primary_key=True)
    assuntoDetalhado = models.TextField(max_length=200)
    dataInicial = models.DateField()
    dataFinal = models.DateField()
    valor = models.FloatField(null=False)
    licitacao_fk= models.ForeignKey("Licitacao", on_delete=models.CASCADE)
    fornecedor_fk = models.ForeignKey("Fornecedor", on_delete=models.CASCADE)
