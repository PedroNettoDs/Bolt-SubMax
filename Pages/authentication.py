from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from Pages.models import PerfilUsuario

class CPFBackend(ModelBackend):
    # Autentica usuários usando CPF em vez de username
    def authenticate(self, request, cpf=None, password=None, **kwargs):
        try:
            perfil = PerfilUsuario.objects.select_related('usuario').get(cpf=cpf)
            user = perfil.usuario
            if user.check_password(password):
                return user
        except PerfilUsuario.DoesNotExist:
            return None
        return None
