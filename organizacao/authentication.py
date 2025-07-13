from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

class CPFBackend(BaseBackend):
    """
    Backend de autenticação por CPF.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Tenta encontrar usuário pelo CPF (assumindo que o username é o CPF)
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

