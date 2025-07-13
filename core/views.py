from django.shortcuts import render
from django.core.paginator import Paginator
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

def alunos_list(request):
    """
    Lista todos os alunos com paginação.
    """
    alunos_list = Aluno.objects.all().order_by('nome')
    paginator = Paginator(alunos_list, 10)  # 10 alunos por página
    
    page_number = request.GET.get('page')
    alunos = paginator.get_page(page_number)
    
    return render(request, 'core/alunos_list.html', {
        'alunos': alunos,
        'is_paginated': alunos.has_other_pages(),
        'page_obj': alunos,
    })

def exercicios_list(request):
    """
    Lista todos os exercícios com paginação.
    """
    exercicios_list = Exercicio.objects.all().order_by('nome')
    paginator = Paginator(exercicios_list, 10)  # 10 exercícios por página
    
    page_number = request.GET.get('page')
    exercicios = paginator.get_page(page_number)
    
    return render(request, 'core/exercicios_list.html', {
        'exercicios': exercicios,
        'is_paginated': exercicios.has_other_pages(),
        'page_obj': exercicios,
    })

def treinos_list(request):
    """
    Lista todos os treinos com paginação.
    """
    treinos_list = Rotina.objects.all().order_by('nome')
    paginator = Paginator(treinos_list, 10)  # 10 treinos por página
    
    page_number = request.GET.get('page')
    treinos = paginator.get_page(page_number)
    
    return render(request, 'core/treinos_list.html', {
        'treinos': treinos,
        'is_paginated': treinos.has_other_pages(),
        'page_obj': treinos,
    })

def avaliacoes_list(request):
    """
    Lista todas as avaliações com paginação.
    """
    avaliacoes_list = Avaliacao.objects.all().order_by('-id')
    paginator = Paginator(avaliacoes_list, 10)  # 10 avaliações por página
    
    page_number = request.GET.get('page')
    avaliacoes = paginator.get_page(page_number)
    
    return render(request, 'core/avaliacoes_list.html', {
        'avaliacoes': avaliacoes,
        'is_paginated': avaliacoes.has_other_pages(),
        'page_obj': avaliacoes,
    })