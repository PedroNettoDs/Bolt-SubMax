from django.contrib import admin
from .models import Avaliacao

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    """
    Configuração da listagem de Avaliações no Django Admin.
    """
    list_display = ("data", "aluno")
    list_filter = ("data", "aluno")
    search_fields = ("aluno", "nome")
