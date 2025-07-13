from django.db import models
from django.contrib.auth.models import User
from organizacao.models import Organizacao

class PerfilUsuario(models.Model):
    """
    Modelo para armazenar informações adicionais do usuário
    """
    NIVEL_ACESSO_CHOICES = [
        ('usuario', 'Usuário'),
        ('admin', 'Administrador'),
        ('master', 'Master')
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    organizacao = models.ForeignKey(Organizacao, on_delete=models.SET_NULL, null=True, blank=True)
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)
    nivel_acesso = models.CharField(max_length=10, choices=NIVEL_ACESSO_CHOICES, default='usuario')
    status_bloqueio = models.BooleanField(default=False)
    primeiro_acesso = models.BooleanField(default=True)

    def __str__(self):
        return self.usuario.username
    
    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuários'