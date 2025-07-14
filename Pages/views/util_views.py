
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect

import math

# Calcula gordura percentual com fórmula de Jackson & Pollock
def calculoGordura(peitoral, abdominal, coxa, triceps, subescapular, suprailiaca, axilar, idade, sexo):
    try:
        soma_dobras = peitoral + abdominal + coxa + triceps + subescapular + suprailiaca + axilar
        if sexo == 'masculino':
            densidade = 1.112 - (0.00043499 * soma_dobras) + (0.00000055 * soma_dobras ** 2) - (0.00028826 * idade)
        elif sexo == 'feminino':
            densidade = 1.097 - (0.00046971 * soma_dobras) + (0.00000056 * soma_dobras ** 2) - (0.00012828 * idade)
        else:
            return None
        return round((495 / densidade) - 450, 2) if densidade else None
    except (TypeError, ValueError):
        return None

# Calcula gordura em kg com fórmula de Jackson & Pollock
def calculoGorduraKg(peitoral, abdominal, coxa, triceps, subescapular, suprailiaca, axilar, idade, sexo, peso):
    try:
        GorduraPorcentual = calculoGordura(peitoral, abdominal, coxa, triceps, subescapular, suprailiaca, axilar, idade, sexo)

        return round((GorduraPorcentual / 100) * peso, 2) if GorduraPorcentual else None
    except (TypeError, ValueError):
        return None


# Calcula massa muscular com base na fórmula de Lee et al. (2000)
def calculadorMusculos(altura, idade, sexo, braco, coxa, panturrilha, dobra_triceps, dobra_coxa, dobra_panturrilha):
    try:
        sexo_valor = 1 if sexo == 'masculino' else 0
        pi = math.pi
        CAG = braco - (pi * (dobra_triceps / 10))
        CT = coxa - (pi * (dobra_coxa / 10))
        CQ = panturrilha - (pi * (dobra_panturrilha / 10))
        massa_muscular = (
            altura * (
                0.00744 * (CAG ** 2) +
                0.00088 * (CT ** 2) +
                0.00441 * (CQ ** 2)
            ) + 2.4 * sexo_valor - 0.048 * idade + 7.8
        )
        return massa_muscular
    except (TypeError, ValueError):
        return None
    
# Função para validar CPF
def validar_cpf(cpf):
    if not cpf or len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    if resto == 10: resto = 0
    if resto != int(cpf[9]):
        return False

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    if resto == 10: resto = 0
    if resto != int(cpf[10]):
        return False

    return True

# Função para remover mensagens pendentes do request
def remover_messages(request):
    list(messages.get_messages(request))  # força o esvaziamento

# Processa a alteração de senha no primeiro acesso

# Processa a alteração de senha no primeiro acesso via AJAX
@login_required
def alterar_senha_primeiro_acesso(request):
    if request.method == "POST":
        import json
        from django.http import JsonResponse

        try:
            data = json.loads(request.body)
            senha_atual = data.get("senha_atual")
            nova_senha = data.get("nova_senha")
            confirmar_senha = data.get("confirmar_senha")
        except Exception:
            return JsonResponse({"success": False, "message": "Erro ao processar dados."})

        # Valida senha forte
        import re
        if len(nova_senha) < 8 or not re.search(r"[A-Z]", nova_senha) or not re.search(r"[a-z]", nova_senha) or not re.search(r"[0-9]", nova_senha):
            return JsonResponse({"success": False, "message": "A senha deve ter pelo menos 8 caracteres, com letras maiúsculas, minúsculas e números."})

        if nova_senha != confirmar_senha:
            return JsonResponse({"success": False, "message": "A nova senha e a confirmação não coincidem."})

        if not request.user.check_password(senha_atual):
            return JsonResponse({"success": False, "message": "Senha atual incorreta."})

        # Altera a senha e atualiza status
        request.user.set_password(nova_senha)
        request.user.save()

        perfil = request.user.perfilusuario
        perfil.primeiro_acesso = False
        perfil.save()

        from django.contrib.auth import update_session_auth_hash
        update_session_auth_hash(request, request.user)

        request.session.pop("forcar_troca_senha", None)

        return JsonResponse({"success": True, "message": "Senha alterada com sucesso."})

