# empresas/management/commands/load_data.py
import csv
import os
from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand
from empresas.models import Empresa

class Command(BaseCommand):
    help = "Importa empresas do novo CSV com UF e capital_social"

    def handle(self, *args, **options):
        csv_path = os.path.join("dados", "dados_cnpj.csv")
        
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f"Arquivo não encontrado: {csv_path}"))
            return

        self.stdout.write("🔍 Lendo novo CSV...")
        
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=",")  # ou ',' se for vírgula
            self.stdout.write(f"📂 Cabeçalhos: {reader.fieldnames[:5]}...")

            batch = []
            total = 0

            for row in reader:
                try:
                    # Processa capital_social com segurança
                    capital_str = row.get("capital_social", "0").strip()
                    capital_clean = capital_str.replace(".", "").replace(",", ".")
                    try:
                        capital = Decimal(capital_clean)
                    except (InvalidOperation, ValueError):
                        capital = Decimal("0.00")

                    empresa = Empresa(
                        cnpj_basico=row["cnpj_basico"],
                        cnpj_ordem=row["cnpj_ordem"],
                        cnpj_dv=row["cnpj_dv"],
                        identificador_matriz_filial=row["identificador_matriz_filial"],
                        nome_fantasia=row.get("nome_fantasia", ""),
                        situacao_cadastral=row["situacao_cadastral"],
                        data_situacao_cadastral=row.get("data_situacao_cadastral", ""),
                        motivo_situacao_cadastral=row.get("motivo_situacao_cadastral", ""),
                        nome_cidade_exterior=row.get("nome_cidade_exterior", ""),
                        pais=row["pais"],
                        data_inicio_atividade=row.get("data_inicio_atividade", ""),
                        cnae_fiscal_principal=row["cnae_fiscal_principal"],
                        cnae_fiscal_secundaria=row.get("cnae_fiscal_secundaria", ""),
                        tipo_logradouro=row.get("tipo_logradouro", ""),
                        logradouro=row.get("logradouro", ""),
                        numero=row.get("numero", ""),
                        complemento=row.get("complemento", ""),
                        bairro=row.get("bairro", ""),
                        cep=row["cep"],
                        uf=row["uf"],  # ✅ Agora temos UF!
                        municipio=row["municipio"],
                        ddd1=row.get("ddd1", ""),
                        telefone1=row.get("telefone1", ""),
                        ddd2=row.get("ddd2", ""),
                        telefone2=row.get("telefone2", ""),
                        ddd_fax=row.get("ddd_fax", ""),
                        fax=row.get("fax", ""),
                        correio_eletronico=row.get("correio_eletronico", ""),
                        situacao_especial=row.get("situacao_especial", ""),
                        data_situacao_especial=row.get("data_situacao_especial", ""),
                        razao_social=row["razao_social"],
                        natureza_juridica=row["natureza_juridica"],
                        qualificacao_responsavel=row["qualificacao_responsavel"],
                        capital_social=capital,
                        porte_empresa=row["porte_empresa"],
                        ente_federativo_responsavel=row.get("ente_federativo_responsavel", ""),
                    )
                    batch.append(empresa)
                    total += 1

                    if len(batch) >= 5000:
                        Empresa.objects.bulk_create(batch, ignore_conflicts=True)
                        self.stdout.write(f"✅ {total} empresas importadas...")
                        batch = []

                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Erro: {e}"))

            if batch:
                Empresa.objects.bulk_create(batch, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS(f"\n🎉 Importação concluída! Total: {total}"))