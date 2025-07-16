from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps
from django.db import connection, OperationalError
from .models import GrupoMuscular
from .constants import MUSCLE_PRESETS


@receiver(post_migrate)
def criar_plano_padrao(sender, **kwargs):
    # Executa apenas para o app Pages
    if sender.name != 'Pages':
        return

    try:
        # Verifica se a tabela Pages_plano existe antes de consultar
        cursor = connection.cursor()
        table_names = connection.introspection.table_names(cursor)
        if 'Pages_plano' not in table_names:
            return
        # Obtém o modelo Plano dinamicamente
        Plano = apps.get_model('Pages', 'Plano')
        if not Plano.objects.filter(nome="Outros").exists():
            Plano.objects.create(nome="Outros")
    except OperationalError:
        # Se houver qualquer erro de banco (tabela não existe), ignora
        pass

@receiver(post_migrate)    
def criar_organizacao_padrao(sender, **kwargs):
    # Executa apenas para o app Pages
    if sender.name != 'Pages':
        return

    try:
        # Verifica se a tabela Pages_organizacao existe
        cursor = connection.cursor()
        table_names = connection.introspection.table_names(cursor)
        if 'Pages_organizacao' not in table_names:
            return

        # Obtém o modelo Organizacao dinamicamente
        Organizacao = apps.get_model('Pages', 'Organizacao')

        # Cria se não existir
        if not Organizacao.objects.filter(nome="Organização Padrão").exists():
            Organizacao.objects.create(nome="Organização Padrão")

    except OperationalError:
        pass  # Ignora erros se o banco ainda não estiver pronto

@receiver(post_migrate)
def create_muscles(sender, app_config, **kwargs):
    """
    Depois de cada `migrate`, insere (ou atualiza) os músculos fixos.
    """

    for slug, nome in MUSCLE_PRESETS.items():
        GrupoMuscular.objects.update_or_create(
            id=slug,
            defaults={'nome': nome}
        )
