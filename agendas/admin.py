from django.contrib import admin
from .models import Agenda

@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    """
    Configuração da listagem de Agendas no Django Admin.
    """
    list_display = ("titulo", "tipo", "aluno", "data", "hora_inicio", "hora_fim")
    list_filter = ("tipo", "data", "aluno")
    search_fields = ("titulo", "descricao", "aluno__nome")
