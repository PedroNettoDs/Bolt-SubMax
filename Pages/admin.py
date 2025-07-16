from django.contrib import admin
from .models import Evento, Aluno, Exercicio, Plano, Avaliacao
from .models import *


# ===================== 2. Cria admins com busca para Aluno/Exercicio ===============

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    # 🔍 Busca por ID, nome ou telefone do aluno
    search_fields = ('id', 'nome', 'telefone')
    list_display = ('id', 'nome', 'telefone', 'email', 'ativo', 'plano_tipo')
    list_filter = ('ativo', 'plano_tipo', 'sexo')


@admin.register(Exercicio)
class ExercicioAdmin(admin.ModelAdmin):
    # 🔍 Busca por ID, nome ou grupo muscular
    search_fields = ('id', 'nome', 'grupo_muscular')
    list_display = ('nome', 'grupo_muscular')
    list_filter = ('nome', 'grupo_muscular')


# ===================== 4. Registra modelos básicos ===============================

admin.site.register(Evento)
admin.site.register(Plano)
admin.site.register(Avaliacao)