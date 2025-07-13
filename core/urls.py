from django.urls import path
from .views import homepage, alunos_list, exercicios_list, treinos_list, avaliacoes_list

urlpatterns = [
    path('', homepage, name='homepage'),  # Rota para a homepage
    path('alunos/', alunos_list, name='alunos_list'),  # Rota para listagem de alunos
    path('exercicios/', exercicios_list, name='exercicios_list'),  # Rota para listagem de exercícios
    path('treinos/', treinos_list, name='treinos_list'),  # Rota para listagem de treinos
    path('avaliacoes/', avaliacoes_list, name='avaliacoes_list'),  # Rota para listagem de avaliações

]