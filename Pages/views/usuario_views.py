from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Pages.models import PerfilUsuario, Organizacao
from .util_views import validar_cpf
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib import messages
import re


# Exibe todos os usuários com seus perfis
@login_required
def usuarios_listagem(request):
    # Verifica se o usuário tem perfil e se é Master
    if not hasattr(request.user, 'perfilusuario') or request.user.perfilusuario.nivel_acesso != 'master':
        messages.error(request, "Acesso restrito ao Master")
        return redirect('home')

    usuarios = User.objects.all().select_related('perfilusuario')
    organizacoes = Organizacao.objects.all()

    return render(request, 'paginas/usuarios.html', {
        'usuarios': usuarios,
        'organizacoes': organizacoes,
    })

# Processa o vínculo entre usuário e organizações
@login_required
def vincular_organizacoes_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    perfil = get_object_or_404(PerfilUsuario, user=usuario)

    if not request.user.perfilusuario.nivel_acesso == 'master':
        return HttpResponseForbidden("Acesso restrito ao Master")

    if request.method == "POST":
        org_ids = request.POST.getlist("organizacoes")
        perfil.organizacoes.set(org_ids)
        return redirect("usuarios_listagem")

def view_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    return render(request, 'paginas/view_usuario.html', {'usuario': usuario})

@login_required
def cadastrar_usuario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome', '')
        sobrenome = request.POST.get('sobrenome', '')
        nivel_acesso = request.POST.get('nivel_acesso', '')
        email = request.POST.get('email', '')
        organizacao_id = request.POST.get('organizacoes', '')

        status_ativo = 'status-user' in request.POST
        status_bloqueio = 'status-user-block' in request.POST

        cpf = request.POST.get("cpf", "")
        cpf_numeros = re.sub(r'\D', '', cpf)

        if not nome or not email or len(cpf_numeros) < 6:
            messages.error(request, 'Erro: Dados obrigatórios ausentes ou CPF inválido.')
            return redirect('usuarios_listagem')

        primeiro_nome = nome.strip().split()[0].lower()
        username = f"{primeiro_nome}{cpf_numeros[-6:]}"
        senha = cpf_numeros[:6]

        if User.objects.filter(username=username).exists():
            messages.error(request, f'Erro: Já existe um usuário com o nome de usuário {username}.')
            return redirect('usuarios_listagem')

        try:
            user = User.objects.create_user(
                username=username,
                first_name=nome,
                last_name=sobrenome,
                password=senha,
                email=email,
                is_active=status_ativo
            )

            organizacao = None
            if organizacao_id:
                try:
                    organizacao = Organizacao.objects.get(id=organizacao_id)
                except Organizacao.DoesNotExist:
                    pass

            PerfilUsuario.objects.create(
                usuario=user,
                cpf=cpf_numeros,
                nivel_acesso=nivel_acesso,
                status_bloqueio=status_bloqueio,
                organizacao=organizacao
            )

            messages.success(
                request,
                f'Usuário cadastrado com sucesso! Senha: 6 primeiros dígitos do CPF.'
            )

        except Exception as e:
            messages.error(request, f'Erro ao cadastrar usuário: {str(e)}')

        return redirect('usuarios_listagem')

    return redirect('usuarios_listagem')

def editar_usuario(request, usuario_id):
    if request.method == 'POST':
        try:
            usuario = get_object_or_404(User, id=usuario_id)
            usuario.first_name = request.POST.get('nome')
            usuario.last_name = request.POST.get('sobrenome')
            usuario.email = request.POST.get('email')
            usuario.save()
            
            try:
                organizacao = Organizacao.objects.get(id=request.POST.get('organizacoes'))
            except Organizacao.DoesNotExist:
                organizacao = None  # opcional

            # Atualiza dados do perfil e organização também
            perfil = usuario.perfilusuario
            perfil.cpf = re.sub(r'\D', '', request.POST.get('cpf'))
            perfil.nivel_acesso = request.POST.get('nivel_acesso')
            perfil.status_bloqueio = bool(request.POST.get('status-user-block'))
            perfil.organizacao = organizacao
            perfil.save()
            
            # Atualiza status ativo
            usuario.is_active = bool(request.POST.get('status-user'))
            usuario.save()
            messages.success(request, 'Usuário editado com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao editar usuário: {str(e)}')

    return redirect('usuarios_listagem')  


def resetar_senha_usuario(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')

        try:
            # Busca o usuário ou retorna 404
            user = get_object_or_404(User, id=usuario_id)

            # Extrai os 6 primeiros dígitos do CPF (apenas números)
            cpf_numeros = ''.join(filter(str.isdigit, user.perfilusuario.cpf))
            nova_senha = cpf_numeros[:6]

            # Define a nova senha e marca primeiro acesso como True
            request.user.set_password(nova_senha)
            request.user.save()
            perfil = request.user.perfilusuario
            perfil.primeiro_acesso = True
            perfil.save()

            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'erro', 'message': str(e)})
    
    return JsonResponse({'status': 'erro', 'message': 'Método inválido'})