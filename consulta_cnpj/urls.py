# urls.py
from django.contrib import admin
from django.urls import path, include
from empresas.views import (
    home,
    cidades_autocomplete,
    empresas_por_cidade,
    naturezas_juridicas,
    empresas_por_natureza_juridica,
    empresas_por_cidade_e_natureza,
    empresas_por_natureza_juridica_parcial,
    empresas_por_cidade_e_natureza_parcial,
    upload_csv,  # nova view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload-csv/', upload_csv, name='upload_csv'),
    path('', home, name='home'),
    path('api/cidades/', cidades_autocomplete, name='cidades_autocomplete'),
    path('api/cidade/<str:cidade>/', empresas_por_cidade, name='empresas_por_cidade'),
    path('api/naturezas/', naturezas_juridicas, name='naturezas_juridicas'),
    path('api/natureza/<str:natureza>/', empresas_por_natureza_juridica, name='empresas_por_natureza_juridica'),
    path('api/natureza/partial/<str:natureza>/', empresas_por_natureza_juridica_parcial, name='empresas_por_natureza_juridica_parcial'),
    
    # ✅ Rota para CIDADE + NATUREZA EXATA (sem /exact/ no caminho)
    path('api/cidade/<str:cidade>/natureza/<str:natureza>/', empresas_por_cidade_e_natureza, name='empresas_por_cidade_e_natureza'),
    
    # ✅ Rota para CIDADE + NATUREZA PARCIAL
    path('api/cidade/<str:cidade>/natureza/partial/<str:natureza>/', empresas_por_cidade_e_natureza_parcial, name='empresas_por_cidade_e_natureza_parcial'),
]