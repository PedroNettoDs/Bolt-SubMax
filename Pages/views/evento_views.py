from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import OperationalError
from Pages.models import Evento, Plano, Aluno
from Pages.utils.db import safe_all, safe_count
from Pages.serializers import EventoSerializer

# Exibe a página principal com eventos e estatísticas
def home_view(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')
        if titulo and data:
            try:
                Evento.objects.create(titulo=titulo, descricao=descricao, data=data)
            except OperationalError:
                # Banco ainda não está pronto, apenas ignora criar evento
                pass
        return redirect('home')

    # Busca eventos
    eventos = safe_all(Evento)

    # Busca planos
    planos = safe_all(Plano)

    # Conta alunos e ativos apenas se tabela existir
    total_alunos = safe_count(Aluno)

    ativos = 0
    if total_alunos > 0:
        if 'ativo' in [f.name for f in Aluno._meta.get_fields()]:
            ativos = safe_count(Aluno.objects.filter(ativo=True))
        else:
            ativos = total_alunos

    percent = round((ativos / total_alunos) * 100) if total_alunos > 0 else 0

    return render(request, 'paginas/home.html', {
        'eventos': eventos,
        'total_alunos': total_alunos,
        'ativos': ativos,
        'percent': percent,
        'planos': planos,
    })

# Retorna eventos em formato JSON para o calendário
@api_view(["GET"])
def eventos_json(request):
    eventos = safe_all(Evento)
    serializer = EventoSerializer(eventos, many=True)
    return Response(serializer.data)
