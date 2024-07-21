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
    cidade = models.CharField(max_length=200)
    telefone = models.CharField(max_length=200)

   #def __str__(self):
    #    return self.nome, self.cnpj, self.endereco, self.num, self.bairro, self.cep, self.cidade, self.telefone
    
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

    def __str__(self):
        return self.assuntoDetalhado

class NotaFiscal(models.Model):
    num = models.IntegerField()
    serie = models.CharField(max_length=15)
    valor = models.FloatField()
    tipo = models.CharField(max_length=50)
    contrato_fk = models.ForeignKey("Contrato", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Notas Fiscais"

    """def __str__(self):
        return self.serie, self.tipo"""
