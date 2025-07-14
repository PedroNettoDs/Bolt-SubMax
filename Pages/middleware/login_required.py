import re
from django.shortcuts import redirect
from django.conf import settings

# Middleware que exige autenticação para todas as páginas, exceto as listadas
class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            re.compile(r'^login/$'),

        ]

    def __call__(self, request):
        path = request.path_info.lstrip('/')
        if not request.user.is_authenticated:
            if not any(pattern.match(path) for pattern in self.exempt_urls):
                return redirect(settings.LOGIN_URL)
        return self.get_response(request)
