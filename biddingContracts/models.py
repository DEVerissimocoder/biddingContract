from django.db import models

#licitacao
class Licitacao (models.Model):
    id_licitacao = models.IntegerField(primary_key=True, auto_created=True)
    numProcess = models.CharField(max_length=7, unique=True)
    categoria = models.CharField(max_length=200, verbose_name="Categoria", null=False)
    assunto = models.CharField(max_length=200, verbose_name="Assunto",  null=False, blank=False)
    date = models.DateField()
    
    def __str__(self):
        return f"{self.assunto}"

    class meta:
        verbose_name = "licitação"
        verbose_name_plural = "licitações"

#Fornecedor
class Fornecedor(models.Model):
    nome = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=200, unique=True)
    endereco = models.CharField(max_length=200)
    num  = models.CharField(max_length=200)
    bairro  = models.CharField(max_length=200)
    cep = models.CharField(max_length=200)
    cidade = models.CharField(max_length=200)
    telefone = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nome}"
    
    class meta:
        verbose_name_plural = "fornecedores"

#Contrato
class Contrato(models.Model):
    id_contrato = models.BigAutoField(primary_key=True, auto_created=True, serialize=True)
    numero = models.CharField(max_length=7, null=False, unique=True, blank=False)
    assuntoDetalhado = models.TextField(max_length=200, verbose_name="Detalhe do contrato", null=False, blank=False)
    dataInicial = models.DateField()
    dataFinal = models.DateField()
    valor = models.FloatField(null=False)
    licitacao_fk= models.ForeignKey("Licitacao", on_delete=models.CASCADE)
    fornecedor_fk = models.ForeignKey("Fornecedor", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.assuntoDetalhado}"

class NotaFiscal(models.Model):
    id_notafiscal = models.BigAutoField(primary_key=True, auto_created=True, serialize=True)
    num = models.IntegerField(unique=True)
    serie = models.CharField(max_length=3)
    valor = models.FloatField()
    tipo = models.CharField(max_length=50)
    dataEmissao = models.DateField()
    contrato_fk = models.ForeignKey("Contrato", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Notas Fiscais"

    def __str__(self):
        return f"{self.tipo}"


class AtaRegistroPreco(models.Model):
    id_arp = models.BigAutoField(primary_key=True, auto_created=True, serialize=True)
    numero = models.CharField( max_length=7, null=False, blank=False)
    assuntoDetalhado = models.TextField(max_length=200, verbose_name="Detalhe do contrato", null=False, blank=False)
    dataInicial = models.DateField()
    dataFinal = models.DateField()
    valor = models.FloatField(null=False)
    licitacao_fk= models.ForeignKey("Licitacao", on_delete=models.CASCADE)
    fornecedor_fk = models.ForeignKey("Fornecedor", on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = 'Atas de Registros de Preços'
    
    