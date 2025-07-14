from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import OperationalError
from Pages.models import Evento, Plano, Aluno

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
    try:
        eventos = Evento.objects.all()
    except OperationalError:
        eventos = []

    # Busca planos
    try:
        planos = Plano.objects.all()
    except OperationalError:
        planos = []

    # Conta alunos e ativos apenas se tabela existir
    try:
        total_alunos = Aluno.objects.count()
    except OperationalError:
        total_alunos = 0

    ativos = 0
    try:
        if total_alunos > 0:
            if 'ativo' in [f.name for f in Aluno._meta.get_fields()]:
                ativos = Aluno.objects.filter(ativo=True).count()
            else:
                ativos = total_alunos
        else:
            ativos = 0
    except OperationalError:
        ativos = 0

    percent = round((ativos / total_alunos) * 100) if total_alunos > 0 else 0

    return render(request, 'paginas/home.html', {
        'eventos': eventos,
        'total_alunos': total_alunos,
        'ativos': ativos,
        'percent': percent,
        'planos': planos,
    })

# Retorna eventos em formato JSON para o calendário
def eventos_json(request):
    try:
        eventos = Evento.objects.all()
        data = [{
            "title": evento.titulo,
            "start": evento.data.isoformat(),
            "description": evento.descricao,
        } for evento in eventos]
    except OperationalError:
        data = []
    return JsonResponse(data, safe=False)