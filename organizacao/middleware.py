from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware(MiddlewareMixin):
    """
    Middleware para exigir login em todas as páginas.
    """
    def process_request(self, request):
        # Lista de URLs que não precisam de login
        exempt_urls = [
            reverse('admin:login'),
            '/login/',
            '/logout/',
        ]
        
        # Se a URL atual está na lista de exceções, permite acesso
        if request.path in exempt_urls:
            return None
            
        # Se o usuário não está autenticado, redireciona para login
        if not request.user.is_authenticated:
            return redirect('/login/')
            
        return None