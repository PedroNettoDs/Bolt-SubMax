from django.shortcuts import render
# TODO: ajustar import caso o nome dos apps mude
from alunos.models import Aluno
from exercicios.models import Exercicio
from treinos.models import Rotina               # FIXME: trocar se o modelo tiver outro nome
from avaliacao.models import Avaliacao          # MELHORIA: criar app 'agendas' futuramente

def homepage(request):
    """
    Dashboard inicial com visão geral de alunos, treinos, exercícios e agendas.
    """
    contexto = {
        # Contagens rápidas para cards/resumos
        "total_alunos": Aluno.objects.count(),
        "total_treinos": Rotina.objects.count(),
        "total_exercicios": Exercicio.objects.count(),
        "total_avaliacoes": Avaliacao.objects.count(),
        
        # Exemplo de listagem curta (últimos 5) – sinta-se livre para remover ou ampliar
        "ultimos_alunos": Aluno.objects.order_by("-id")[:5],
        "ultimos_treinos": Rotina.objects.order_by("-id")[:5],
    }
    # Renderiza template localizado em core/templates/core/homepage.html
    return render(request, "core/homepage.html", contexto)
