from django.urls import path
from .views import (
    homepage,
    alunos_list,
    exercicios_list,
    treinos_list,
    avaliacoes_list,
    aluno_create,
    exercicio_create,
    treino_create,
    avaliacao_create,
)

urlpatterns = [
    path('', homepage, name='homepage'),
    path('alunos/', alunos_list, name='alunos_list'),
    path('alunos/novo/', aluno_create, name='aluno_create'),
    path('exercicios/', exercicios_list, name='exercicios_list'),
    path('exercicios/novo/', exercicio_create, name='exercicio_create'),
    path('treinos/', treinos_list, name='treinos_list'),
    path('treinos/novo/', treino_create, name='treino_create'),
    path('avaliacoes/', avaliacoes_list, name='avaliacoes_list'),
    path('avaliacoes/novo/', avaliacao_create, name='avaliacao_create'),
]
