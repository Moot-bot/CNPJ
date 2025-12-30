# ingest_csv.py
import os
import csv
from psycopg2 import connect
from psycopg2.extras import execute_values

# 🔒 Substitua pela External Database URL do Render (plano pago)
DATABASE_URL = os.getenv("postgresql://cnpj_db_user:ch7xeNfQE1Ddr7BbP4hiogvBnyKItlsY@dpg-d59tik1r0fns73814cdg-a.oregon-postgres.render.com/cnpj_db")

def get_connection():
    return connect(DATABASE_URL)

def ingest():
    if not DATABASE_URL:
        raise ValueError("❌ Defina DATABASE_URL como variável de ambiente!")

    conn = get_connection()
    cur = conn.cursor()

    print("🔍 Iniciando ingestão do CSV...")

    with open("dados_cnpj.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        batch = []
        count = 0

        for row in reader:
            try:
                # Converter capital_social para float (substitui vírgula por ponto se necessário)
                capital = row["capital_social"].replace(",", ".") if row["capital_social"] else "0.0"
                capital = float(capital) if capital else 0.0

                batch.append((
                    row["cnpj_basico"],
                    row["cnpj_ordem"],
                    row["cnpj_dv"],
                    row["identificador_matriz_filial"],
                    row["nome_fantasia"],
                    row["situacao_cadastral"],
                    row["data_situacao_cadastral"],
                    row["motivo_situacao_cadastral"],
                    row["nome_cidade_exterior"],
                    row["pais"],
                    row["data_inicio_atividade"],
                    row["cnae_fiscal_principal"],
                    row["cnae_fiscal_secundaria"],
                    row["tipo_logradouro"],
                    row["logradouro"],
                    row["numero"],
                    row["complemento"],
                    row["bairro"],
                    row["cep"],
                    row["uf"],
                    row["ddd1"],
                    row["telefone1"],
                    row["ddd2"],
                    row["telefone2"],
                    row["ddd_fax"],
                    row["fax"],
                    row["correio_eletronico"],
                    row["situacao_especial"],
                    row["data_situacao_especial"],
                    row["razao_social"],
                    row["qualificacao_responsavel"],
                    capital,
                    row["porte_empresa"],
                    row["ente_federativo_responsavel"],
                    row["municipio"],
                    row["natureza_juridica"],
                ))

                if len(batch) >= 10_000:
                    execute_values(
                        cur,
                        """
                        INSERT INTO empresas_empresa (
                            cnpj_basico, cnpj_ordem, cnpj_dv, identificador_matriz_filial,
                            nome_fantasia, situacao_cadastral, data_situacao_cadastral,
                            motivo_situacao_cadastral, nome_cidade_exterior, pais,
                            data_inicio_atividade, cnae_fiscal_principal, cnae_fiscal_secundaria,
                            tipo_logradouro, logradouro, numero, complemento, bairro, cep, uf,
                            ddd1, telefone1, ddd2, telefone2, ddd_fax, fax, correio_eletronico,
                            situacao_especial, data_situacao_especial, razao_social,
                            qualificacao_responsavel, capital_social, porte_empresa,
                            ente_federativo_responsavel, municipio, natureza_juridica
                        ) VALUES %s
                        """,
                        batch,
                    )
                    conn.commit()
                    count += len(batch)
                    print(f"✅ {count:,} registros inseridos...")
                    batch = []

            except Exception as e:
                print(f"⚠️ Erro na linha {count + len(batch) + 1}: {e}")
                continue

        # Inserir lote final
        if batch:
            execute_values(
                cur,
                """
                INSERT INTO empresas_empresa (
                    cnpj_basico, cnpj_ordem, cnpj_dv, identificador_matriz_filial,
                    nome_fantasia, situacao_cadastral, data_situacao_cadastral,
                    motivo_situacao_cadastral, nome_cidade_exterior, pais,
                    data_inicio_atividade, cnae_fiscal_principal, cnae_fiscal_secundaria,
                    tipo_logradouro, logradouro, numero, complemento, bairro, cep, uf,
                    ddd1, telefone1, ddd2, telefone2, ddd_fax, fax, correio_eletronico,
                    situacao_especial, data_situacao_especial, razao_social,
                    qualificacao_responsavel, capital_social, porte_empresa,
                    ente_federativo_responsavel, municipio, natureza_juridica
                ) VALUES %s
                """,
                batch,
            )
            conn.commit()
            count += len(batch)
            print(f"✅ Total final: {count:,} registros inseridos.")

    cur.close()
    conn.close()
    print("🎉 Ingestão concluída com sucesso!")

if __name__ == "__main__":
    ingest()