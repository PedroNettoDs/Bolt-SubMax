from django.contrib import admin
from .models import PerfilUsuario

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    """
    Configuração da listagem de Perfis de Usuários no Django Admin.
    """
    list_display = ("usuario", "nivel_acesso", "status_bloqueio", "primeiro_acesso")
    list_filter = ("nivel_acesso", "status_bloqueio")
    search_fields = ("usuario__username", "cpf")
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('usuario', 'organizacao')