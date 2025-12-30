from django.db import models
class ImportStatus(models.Model):
    key = models.CharField(max_length=50, unique=True)
    done = models.BooleanField(default=False)

class Empresa(models.Model):
    cnpj_basico = models.CharField(max_length=8)
    cnpj_ordem = models.CharField(max_length=4)
    cnpj_dv = models.CharField(max_length=2)
    identificador_matriz_filial = models.CharField(max_length=1)
    nome_fantasia = models.CharField(max_length=200, blank=True)
    situacao_cadastral = models.CharField(max_length=30)
    data_situacao_cadastral = models.CharField(max_length=10, blank=True)  # ou use DateField se converter
    motivo_situacao_cadastral = models.CharField(max_length=10, blank=True)
    nome_cidade_exterior = models.CharField(max_length=100, blank=True)
    pais = models.CharField(max_length=100)
    data_inicio_atividade = models.CharField(max_length=10, blank=True)
    cnae_fiscal_principal = models.CharField(max_length=10)
    cnae_fiscal_secundaria = models.TextField(blank=True)
    tipo_logradouro = models.CharField(max_length=20, blank=True)
    logradouro = models.CharField(max_length=200, blank=True)
    numero = models.CharField(max_length=10, blank=True)
    complemento = models.CharField(max_length=200, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    cep = models.CharField(max_length=10)
    uf = models.CharField(max_length=2)  # ← AGORA TEMOS UF!
    municipio = models.CharField(max_length=100)
    ddd1 = models.CharField(max_length=4, blank=True)
    telefone1 = models.CharField(max_length=10, blank=True)
    ddd2 = models.CharField(max_length=4, blank=True)
    telefone2 = models.CharField(max_length=10, blank=True)
    ddd_fax = models.CharField(max_length=4, blank=True)
    fax = models.CharField(max_length=10, blank=True)
    correio_eletronico = models.CharField(max_length=100, blank=True)
    situacao_especial = models.CharField(max_length=100, blank=True)
    data_situacao_especial = models.CharField(max_length=10, blank=True)
    razao_social = models.CharField(max_length=200)
    natureza_juridica = models.CharField(max_length=255)
    qualificacao_responsavel = models.CharField(max_length=100)
    capital_social = models.DecimalField(max_digits=15, decimal_places=2)
    porte_empresa = models.CharField(max_length=50)
    ente_federativo_responsavel = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.cnpj_basico} - {self.razao_social}"

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"