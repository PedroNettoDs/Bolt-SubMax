from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.db import connection, OperationalError

@receiver(post_migrate)
def criar_plano_padrao(sender, **kwargs):
    # Executa apenas para o app alunos
    if sender.name != 'alunos':
        return

    try:
        # Verifica se a tabela alunos_plano existe antes de consultar
        cursor = connection.cursor()
        table_names = connection.introspection.table_names(cursor)
        if 'alunos_plano' not in table_names:
            return
        
        # Obtém o modelo Plano dinamicamente
        from alunos.models import Plano
        if not Plano.objects.filter(nome="Outros").exists():
            Plano.objects.create(nome="Outros", descricao="Plano padrão para categorização geral")
    except OperationalError:
        # Se houver qualquer erro de banco (tabela não existe), ignora
        pass