from Pages.models import PerfilUsuario
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
import re, json

def login_usuario(request):
    if request.method == "POST":
        # Detecta se é JSON (AJAX) ou form HTML tradicional
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json'

        try:
            if is_ajax:
                data = json.loads(request.body)
                cpf = re.sub(r'\D', '', data.get("cpf", ""))
                senha = data.get("password", "")
            else:
                cpf = re.sub(r'\D', '', request.POST.get("cpf", ""))
                senha = request.POST.get("password", "")
        except Exception:
            cpf = senha = ""

        if not cpf or not senha:
            msg = "Digite um CPF ou SENHA."
            if is_ajax:
                return JsonResponse({"success": False, "message": msg, "level": "warning"}, status=400)
            return redirect("login")

        user = authenticate(request, cpf=cpf, password=senha)

        if user is not None:
            if not user.is_active:
                msg = "Usuário desativado. Contate o administrador."
                if is_ajax:
                    return JsonResponse({"success": False, "message": msg, "level": "danger"}, status=403)
                return render(request, "paginas/login.html")

            login(request, user)

            # Verifica se é o primeiro acesso e define a flag para exibir o modal
            try:
                perfil = request.user.perfilusuario
                if perfil.primeiro_acesso:
                    request.session['forcar_troca_senha'] = True
            except PerfilUsuario.DoesNotExist:
                pass

            if is_ajax:
                return JsonResponse({"success": True, "redirect_url": "/home/"})
            return redirect("home")
        else:
            msg = "CPF ou senha inválidos."
            if is_ajax:
                return JsonResponse({"success": False, "message": msg, "level": "danger"}, status=401)
            return redirect("login")

    # GET request — renderiza a página de login normalmente
    return render(request, "paginas/login.html")

# View de logout
def logout_usuario(request):
    logout(request)
    return redirect("login")

