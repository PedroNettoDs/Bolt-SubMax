from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.db import connection, OperationalError
from django.contrib.auth.models import User

@receiver(post_migrate)
def criar_organizacao_padrao(sender, **kwargs):
    # Executa apenas para o app organizacao
    if sender.name != 'organizacao':
        return

    try:
        # Verifica se a tabela organizacao_organizacao existe
        cursor = connection.cursor()
        table_names = connection.introspection.table_names(cursor)
        if 'organizacao_organizacao' not in table_names:
            return

        # Obtém o modelo Organizacao dinamicamente
        from organizacao.models import Organizacao

        # Cria se não existir
        if not Organizacao.objects.filter(nome="Organização Padrão").exists():
            Organizacao.objects.create(nome="Organização Padrão")

    except OperationalError:
        pass  # Ignora erros se o banco ainda não estiver pronto

@receiver(post_save, sender=User)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    """Cria um perfil de usuário automaticamente quando um usuário é criado"""
    if created:
        try:
            from organizacao.models import Organizacao
            from core.models import PerfilUsuario
            
            # Obtém a organização padrão ou cria se não existir
            org_padrao, _ = Organizacao.objects.get_or_create(nome="Organização Padrão")
            
            # Cria o perfil do usuário
            PerfilUsuario.objects.create(
                usuario=instance,
                organizacao=org_padrao,
                nivel_acesso='usuario'
            )
        except Exception as e:
            print(f"Erro ao criar perfil de usuário: {e}")