from django.contrib import admin
from .models import Evento, Aluno, Exercicio, Plano, Avaliacao
from .models import TreinoAluno, TreinoAlunoExercicio

# ===================== 1. Ajusta Inlines que usam autocomplete =====================

class TreinoAlunoExercicioInline(admin.TabularInline):
    model = TreinoAlunoExercicio
    extra = 1
    autocomplete_fields = ['exercicio']
    # 🔍 Mesmo critério de busca
    search_fields = ('id', 'exercicio__nome')


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


# ===================== 3. Admins para modelos de treino ===============================

@admin.register(TreinoAluno)
class TreinoAlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'aluno', 'data_inicio', 'data_fim', 'criado_em')
    search_fields = ('nome', 'aluno__nome')
    list_filter = ('data_inicio', 'criado_em')
    autocomplete_fields = ['aluno']
    inlines = [TreinoAlunoExercicioInline]


# ===================== 4. Registra modelos básicos ===============================

admin.site.register(Evento)
admin.site.register(Plano)
admin.site.register(Avaliacao)