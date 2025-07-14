from .auth_views import login_usuario, logout_usuario
from .evento_views import home_view, eventos_json
from .aluno_views import alunos_view, cadastrar_aluno, atualizar_aluno, lista_alunos, importar_excel
from .avaliacao_views import view_aluno, cadastrar_avaliacao, editar_avaliacao
from .treino_views import treinos_view, pagina_treinos, cadastrar_treino, cadastrar_exercicio
from .usuario_views import usuarios_listagem, vincular_organizacoes_usuario, view_usuario, cadastrar_usuario