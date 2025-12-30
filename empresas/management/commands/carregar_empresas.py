# carregar_empresas.py
import csv
import zipfile
from django.core.management.base import BaseCommand
from empresas.models import Empresa
import os

class Command(BaseCommand):
    help = 'Carrega empresas a partir do CSV compactado'

    def handle(self, *args, **options):
        # Caminho do ZIP
        zip_path = os.path.join('dados', 'empresas.csv.zip')
        csv_filename = 'seu_arquivo.csv'  # ← ALTERE para o nome real do CSV DENTRO do ZIP

        self.stdout.write("📦 Descompactando CSV...")
        with zipfile.ZipFile(zip_path, 'r') as z:
            with z.open(csv_filename) as f:
                # Decodifica de bytes para string
                reader = csv.DictReader(
                    (line.decode('utf-8') for line in f),
                    delimiter=',',
                    quotechar='"'
                )
                self.stdout.write(f"📥 Lendo registros...")
                count = 0
                for row in reader:
                    try:
                        Empresa.objects.create(
                            # 🔁 Mapeie os campos EXATOS do seu CSV para o model
                            cnpj_basico=row['cnpj_basico'],
                            razao_social=row['razao_social'],
                            nome_fantasia=row.get('nome_fantasia', ''),
                            natureza_juridica=row['natureza_juridica'],
                            porte_empresa=row['porte_empresa'],
                            capital_social=float(row['capital_social']) if row['capital_social'] else 0.0,
                            uf=row['uf'],
                            municipio=row['municipio'],
                            cep=row.get('cep', ''),
                            logradouro=row.get('logradouro', ''),
                            numero=row.get('numero', ''),
                            bairro=row.get('bairro', ''),
                            telefone1=row.get('telefone1', ''),
                            telefone2=row.get('telefone2', ''),
                            correio_eletronico=row.get('correio_eletronico', ''),
                        )
                        count += 1
                        if count % 10000 == 0:
                            self.stdout.write(f"   {count} registros inseridos...")
                    except Exception as e:
                        self.stdout.write(f"⚠️ Erro na linha {count+1}: {e}")
                        continue

        self.stdout.write(self.style.SUCCESS(f'✅ {count} empresas carregadas com sucesso!'))