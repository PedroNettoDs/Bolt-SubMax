from django.contrib import admin
from .models import Rotina

@admin.register(Rotina)
class RotinaAdmin(admin.ModelAdmin):
    """
    Configuração da listagem de Rotinas no Django Admin.
    """
    list_display = ("aluno", "nome", "data_inicio", "data_fim", "criado_em")
    list_filter = ("aluno", "nome", "criado_em")
    search_fields = ("nome", "aluno")