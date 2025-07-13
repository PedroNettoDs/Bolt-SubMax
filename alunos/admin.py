from django.contrib import admin
from .models import Aluno, Plano

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    """
    Configuração da listagem de Alunos no Django Admin.
    """
    list_display = ("organizacao", "ativo", "nome", "email", "telefone")
    list_filter = ("nome", "email", "telefone")
    search_fields = ("nome", "email", "telefone")

@admin.register(Plano)
class PlanoAdmin(admin.ModelAdmin):
    """
    Configuração da listagem de Planos no Django Admin.
    """
    list_display = ("nome", "descricao")
    search_fields = ("nome",)