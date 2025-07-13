from django.contrib import admin
from .models import Organizacao

@admin.register(Organizacao)
class OrganizacaoAdmin(admin.ModelAdmin):
    """
    Configuração da listagem de Organizações no Django Admin.
    """
    list_display = ("nome", "cnpj", "telefone", "criacao")
    list_filter = ("criacao",)
    search_fields = ("nome", "cnpj", "telefone")