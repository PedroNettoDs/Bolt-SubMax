from Pages.views.util_views import alterar_senha_primeiro_acesso
from django.urls import path, include
from .views.evento_views import *
from .views.aluno_views import *
from .views.usuario_views import *
from .views.avaliacao_views import *
from .views.treino_views import *
from .views.auth_views import *
from .views.exercico_views import *
from .views import treino_views



from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'grupos-musculares', GrupoMuscularViewSet)
router.register(r'exercicios', ExercicioViewSet, basename='exercicio')
router.register(r'treinos-aluno', TreinoAlunoViewSet, basename='treino-aluno')



urlpatterns = [
    path('alterar-senha-primeiro-acesso/', alterar_senha_primeiro_acesso, name='alterar_senha_primeiro_acesso'),

    path('', login_usuario, name='login'),
    path('home/', home_view, name='home'),
    path('logout/', logout_usuario, name='logout'),

    # Alunos
    path('alunos/', alunos_view, name='alunos'),
    path('lista_alunos/', lista_alunos, name='lista_alunos'),
    path('cadastrar_aluno/', cadastrar_aluno, name='cadastrar_aluno'),
    path('importar_excel/', importar_excel, name='importar_excel'),
    path('aluno/<int:aluno_id>/', view_aluno, name='view_aluno'),
    path('aluno/<int:aluno_id>/atualizar/', atualizar_aluno, name='atualizar_aluno'),

    # Avaliações
    path('aluno/<int:aluno_id>/avaliacao/cadastrar/', cadastrar_avaliacao, name='cadastrar_avaliacao'),
    path('avaliacoes/<int:avaliacao_id>/editar/', editar_avaliacao, name='editar_avaliacao'),
    path('aluno/<int:aluno_id>/atualizardadospessoais/', atualizar_dados_complementares, name='atualizar_dados_complementares'),
    
    # Treinos
    path('api/treinos/<int:treino_id>/exercicios/', treino_exercicios, name='treino_exercicios'),
    path('treinos/', treino_views.treinos_view, name='treinos'),

    

    # Exercícios
    path('exercicios_json/', exercicios_json, name='exercicios_json'),
    path('salvar_treino/', salvar_treino, name='salvar_treino'),
    path("api/", include(router.urls)),

    # Eventos
    path('eventos_json/', eventos_json, name='eventos_json'),

    # Usuario
    path('usuarios/', usuarios_listagem, name='usuarios_listagem'),
    path('usuarios/vincular-organizacoes/<int:usuario_id>/', vincular_organizacoes_usuario, name='vincular_organizacoes_usuario'),
    path("login/", login_usuario, name="login"),
    path("logout/", logout_usuario, name="logout"),
    path('usuarios/<int:usuario_id>/', view_usuario, name='view_usuario'),
    path('usuarios/cadastrar/', cadastrar_usuario, name='cadastrar_usuario'),
    path('editar_usuario/<int:usuario_id>/', editar_usuario, name='editar_usuario'),
    path('resetar-senha/', resetar_senha_usuario, name='resetar_senha_usuario'),

]


from .views.treino_views import TreinoAlunoListCreateAPIView # Assumindo a view em treino_views

urlpatterns.append(
    path("api/treinos-aluno/", TreinoAlunoListCreateAPIView.as_view(), name="treino-aluno-list-create")
)
