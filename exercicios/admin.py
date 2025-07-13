from django.contrib import admin
from .models import Exercicio, GrupoMuscular

@admin.register(Exercicio)
class ExercicioAdmin(admin.ModelAdmin):
    """
    Configuração da listagem de Exercícios no Django Admin.
    """
    list_display = ("nome", "descricao", "grupo_muscular", "grupo_muscular_secundario")
    list_filter = ("nome",)
    search_fields = ("nome", "descricao")

@admin.register(GrupoMuscular)
class GrupoMuscularAdmin(admin.ModelAdmin):
    """
    Configuração da listagem de Grupos Musculares no Django Admin.
    """
    list_display = ("id", "nome")
    search_fields = ("nome",)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.order_by('nome')
