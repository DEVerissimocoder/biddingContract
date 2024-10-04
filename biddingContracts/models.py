from django.db import models
from django.utils import timezone


class Modalidade(models.TextChoices):
    CONCORRENCIA = 'concorrência', 'Concorrência'
    PREGAO = 'pregao', 'Pregão'
    LEILAO = 'leilao', 'Leilão'
    CONCURSO = 'concurso', 'Concurso'
    DIALOGO_COMPETITIVO = 'dialogo_competitivo', 'Diálogo Competitivo'

class Licitacao (models.Model):
    numProcess = models.CharField(max_length=7, unique=True, blank=False, null=False)
    categoria = models.CharField(max_length=150, choices=Modalidade.choices)
    assunto = models.CharField(max_length=200, verbose_name="Assunto",  null=False, blank=False)
    date = models.DateField()
    
    def __str__(self):
        return f"{self.numProcess}"

    class Meta:
        verbose_name = "licitação"
        verbose_name_plural = "licitações"

#Fornecedor
class Fornecedor(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome do fornecedor", null=False, blank=False)
    cnpj = models.CharField(max_length=200, unique=True, verbose_name="Cadastro de Pessoa Jurídica", null=False, blank=False)
    endereco = models.CharField(max_length=200)
    num  = models.CharField(max_length=200)
    bairro  = models.CharField(max_length=200)
    cep = models.CharField(max_length=200)
    cidade = models.CharField(max_length=200)
    telefone = models.CharField(max_length=200)
    uf = models.CharField(max_length=2, null=True)

    def __str__(self):
        return f"{self.nome}"
    
    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "fornecedores"

#Contrato
class Contrato(models.Model):
    numero = models.CharField(max_length=7, null=False, unique=True, blank=False)
    assuntoDetalhado = models.TextField(max_length=200, verbose_name="Detalhe do contrato", null=False, blank=False)
    dataInicial = models.DateField()
    dataFinal = models.DateField()
    valor = models.FloatField(null=False)
    licitacao_fk= models.ForeignKey("Licitacao", on_delete=models.CASCADE)
    fornecedor_fk = models.ForeignKey("Fornecedor", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.numero}"
    

    def is_vencido(self):
        # Verifica se a data final do contrato já passou
        return self.dataFinal < timezone.now().date()

class NotaFiscal(models.Model):
    num = models.IntegerField(unique=True)
    serie = models.CharField(max_length=3)
    valor = models.FloatField()
    tipo = models.CharField(max_length=50)
    dataEmissao = models.DateField()
    contrato_fk = models.ForeignKey("Contrato", blank=True, null=True, on_delete=models.CASCADE)
    fornecedor_fk = models.ForeignKey("Fornecedor", on_delete=models.CASCADE)
    ataregistropreco_fk = models.ForeignKey('AtaRegistroPreco', blank=True, null=True, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Notas Fiscais"

    def __str__(self):
        return f"{self.tipo}"


class AtaRegistroPreco(models.Model):
    numero = models.CharField( max_length=7, null=False, blank=False)
    assuntoDetalhado = models.TextField(max_length=200, verbose_name="Detalhe do contrato", null=False, blank=False)
    dataInicial = models.DateField()
    dataFinal = models.DateField()
    valor = models.FloatField(null=False)
    licitacao_fk= models.ForeignKey("Licitacao", on_delete=models.CASCADE)
    fornecedor_fk = models.ForeignKey("Fornecedor", on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.numero}'
    
    class Meta:
        verbose_name_plural = 'Atas de Registros de Preços'
    
    