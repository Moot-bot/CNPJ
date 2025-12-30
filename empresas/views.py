import unicodedata
from django.http import JsonResponse
from django.shortcuts import render
from empresas.models import Empresa
from urllib.parse import unquote
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
import csv

@csrf_exempt
@require_http_methods(["POST"])
def upload_csv(request):
    # 🔑 Defina aqui a senha que você usará no curl
    auth_key = request.headers.get("X-Auth-Key")
    if auth_key != "sua_senha_secreta_aqui":  # ← Substitua por algo forte depois
        return JsonResponse({"error": "Unauthorized"}, status=403)

    csv_file = request.FILES.get("file")
    if not csv_file:
        return JsonResponse({"error": "No file provided"}, status=400)

    decoded_file = csv_file.read().decode("utf-8").splitlines()
    reader = csv.DictReader(decoded_file)

    count = 0
    for row in reader:
        try:
            capital_str = row.get("capital_social", "0").replace(",", ".")
            capital = float(capital_str) if capital_str.replace(".", "").isdigit() else 0.0

            Empresa.objects.create(
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
                capital_social=capital,
                porte_empresa=row["porte_empresa"],
                ente_federativo_responsavel=row["ente_federativo_responsavel"],
                municipio=row["municipio"],
                natureza_juridica=row["natureza_juridica"],
            )
            count += 1
            if count % 1000 == 0:
                print(f"{count} registros inseridos...")
        except Exception as e:
            print(f"Erro na linha {count + 1}: {e}")
            continue

    return JsonResponse({"success": f"{count} registros inseridos"})


def remover_acentos(texto):
    """Remove acentos de uma string"""
    if not isinstance(texto, str):
        return ''
    return ''.join(
        char for char in unicodedata.normalize('NFD', texto)
        if unicodedata.category(char) != 'Mn'
    ).upper()


# ======================
# Views
# ======================

def home(request):
    return render(request, 'index.html')


def cidades_autocomplete(request):
    termo = request.GET.get('q', '').strip()
    if len(termo) < 2:
        return JsonResponse([], safe=False)

    cidades = (
        Empresa.objects
        .filter(municipio__icontains=termo)
        .values('municipio', 'uf')
        .distinct()
        .order_by('municipio')
    )[:15]

    resultado = [
        {
            "label": f"{c['municipio']} ({c['uf']})",
            "value": c['municipio']
        }
        for c in cidades
    ]
    return JsonResponse(resultado, safe=False)


def empresas_por_cidade(request, cidade):
    offset = int(request.GET.get('offset', 0))
    empresas = Empresa.objects.filter(
        municipio__iexact=cidade
    ).order_by('-capital_social').values(
        'cnpj_basico',
        'razao_social',
        'nome_fantasia',
        'porte_empresa',
        'capital_social',
        'uf',
        'municipio',
        'cep',
        'logradouro',
        'numero',
        'bairro',
        'telefone1',
        'telefone2',
        'correio_eletronico'
    )[offset:offset + 100]
    return JsonResponse(list(empresas), safe=False)


def naturezas_juridicas(request):
    naturezas = (
        Empresa.objects
        .values_list('natureza_juridica', flat=True)
        .distinct()
        .order_by('natureza_juridica')
    )
    return JsonResponse(list(naturezas), safe=False)


def empresas_por_natureza_juridica(request, natureza):
    offset = int(request.GET.get('offset', 0))
    empresas = Empresa.objects.filter(
        natureza_juridica__iexact=natureza
    ).order_by('-capital_social').values(
        'cnpj_basico',
        'razao_social',
        'nome_fantasia',
        'porte_empresa',
        'capital_social',
        'uf',
        'municipio',
        'cep',
        'logradouro',
        'numero',
        'bairro',
        'telefone1',
        'telefone2',
        'correio_eletronico'
    )[offset:offset + 100]
    return JsonResponse(list(empresas), safe=False)


def empresas_por_natureza_juridica_parcial(request, natureza):
    offset = int(request.GET.get('offset', 0))
    empresas = Empresa.objects.filter(
        natureza_juridica__icontains=natureza
    ).order_by('-capital_social').values(
        'cnpj_basico',
        'razao_social',
        'nome_fantasia',
        'porte_empresa',
        'capital_social',
        'uf',
        'municipio',
        'cep',
        'logradouro',
        'numero',
        'bairro',
        'telefone1',
        'telefone2',
        'correio_eletronico'
    )[offset:offset + 100]
    return JsonResponse(list(empresas), safe=False)


def empresas_por_cidade_e_natureza(request, cidade, natureza):
    offset = int(request.GET.get('offset', 0))
    empresas = Empresa.objects.filter(
        municipio__iexact=cidade,
        natureza_juridica__iexact=natureza
    ).order_by('-capital_social').values(
        'cnpj_basico',
        'razao_social',
        'nome_fantasia',
        'porte_empresa',
        'capital_social',
        'uf',
        'municipio',
        'cep',
        'logradouro',
        'numero',
        'bairro',
        'telefone1',
        'telefone2',
        'correio_eletronico'
    )[offset:offset + 100]
    return JsonResponse(list(empresas), safe=False)


def empresas_por_cidade_e_natureza_parcial(request, cidade, natureza):
    offset = int(request.GET.get('offset', 0))

    cidade = unquote(cidade)
    natureza = unquote(natureza)

    empresas = Empresa.objects.filter(
        municipio__icontains=cidade,
        natureza_juridica__icontains=natureza
    ).order_by('-capital_social').values(
        'cnpj_basico',
        'razao_social',
        'nome_fantasia',
        'porte_empresa',
        'capital_social',
        'uf',
        'municipio',
        'cep',
        'logradouro',
        'numero',
        'bairro',
        'telefone1',
        'telefone2',
        'correio_eletronico'
    )[offset:offset + 100]

    return JsonResponse(list(empresas), safe=False)
