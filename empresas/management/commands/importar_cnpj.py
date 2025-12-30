import csv
import zipfile
import requests
from io import BytesIO, TextIOWrapper
from django.core.management.base import BaseCommand
from empresas.models import Empresa

GITHUB_ZIP_URL = "https://github.com/Moot-bot/CNPJ/releases/download/dados-v1/dados_cnpj.zip"

class Command(BaseCommand):
    help = "Importa dados do CNPJ a partir do GitHub Releases"

    def handle(self, *args, **options):
        self.stdout.write("📥 Baixando arquivo do GitHub...")

        response = requests.get(GITHUB_ZIP_URL, stream=True)
        response.raise_for_status()

        zip_file = zipfile.ZipFile(BytesIO(response.content))

        csv_name = zip_file.namelist()[0]

        self.stdout.write(f"📄 Lendo arquivo {csv_name}")

        file = zip_file.open(csv_name)
        reader = csv.DictReader(TextIOWrapper(file, encoding="utf-8"))

        empresas = []
        total = 0
        BATCH_SIZE = 1000

        for row in reader:
            empresas.append(Empresa(
                cnpj_basico=row["cnpj_basico"],
                cnpj_ordem=row["cnpj_ordem"],
                cnpj_dv=row["cnpj_dv"],
                identificador_matriz_filial=row["identificador_matriz_filial"],
                nome_fantasia=row["nome_fantasia"],
                situacao_cadastral=row["situacao_cadastral"],
                data_situacao_cadastral=row["data_situacao_cadastral"],
                motivo_situacao_cadastral=row["motivo_situacao_cadastral"],
                nome_cidade_exterior=row["nome_cidade_exterior"],
                pais=row["pais"],
                data_inicio_atividade=row["data_inicio_atividade"],
                cnae_fiscal_principal=row["cnae_fiscal_principal"],
                cnae_fiscal_secundaria=row["cnae_fiscal_secundaria"],
                tipo_logradouro=row["tipo_logradouro"],
                logradouro=row["logradouro"],
                numero=row["numero"],
                complemento=row["complemento"],
                bairro=row["bairro"],
                cep=row["cep"],
                uf=row["uf"],
                ddd1=row["ddd1"],
                telefone1=row["telefone1"],
                ddd2=row["ddd2"],
                telefone2=row["telefone2"],
                ddd_fax=row["ddd_fax"],
                fax=row["fax"],
                correio_eletronico=row["correio_eletronico"],
                situacao_especial=row["situacao_especial"],
                data_situacao_especial=row["data_situacao_especial"],
                razao_social=row["razao_social"],
                qualificacao_responsavel=row["qualificacao_responsavel"],
                capital_social=float(row["capital_social"].replace(",", ".")) if row["capital_social"] else 0,
                porte_empresa=row["porte_empresa"],
                ente_federativo_responsavel=row["ente_federativo_responsavel"],
                municipio=row["municipio"],
                natureza_juridica=row["natureza_juridica"],
            ))

            if len(empresas) >= BATCH_SIZE:
                Empresa.objects.bulk_create(empresas, ignore_conflicts=True)
                total += len(empresas)
                empresas.clear()
                self.stdout.write(f"✔ {total} registros inseridos")

        if empresas:
            Empresa.objects.bulk_create(empresas, ignore_conflicts=True)
            total += len(empresas)

        self.stdout.write(self.style.SUCCESS(f"🚀 Importação finalizada: {total} registros"))
