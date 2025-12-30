from django.contrib import admin
from .models import Empresa

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['cnpj_basico', 'razao_social', 'porte_empresa']
    search_fields = ['cnpj_basico', 'razao_social']
    list_filter = ['porte_empresa']