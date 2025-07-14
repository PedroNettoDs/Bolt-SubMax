from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from Pages.models import (
    Exercicio, Treino, Aluno, ExercicioTreino,
    TreinoPredefinido, TreinoPredefExercicio,
    TreinoAluno, TreinoAlunoExercicio
)
import json
from datetime import date

# Página de treinos
def treinos_view(request):
    """
    Exibe a página de treinos com filtros e paginação de 8 itens por página
    """
    # Busca Exercício
    busca_exercicio = request.GET.get('busca_exercicio', '').strip()
    # Busca Treino
    busca_treino = request.GET.get('busca_treino', '').strip()

    # Consulta Exercícios com filtro
    exercicios_qs = Exercicio.objects.all()
    if busca_exercicio:
        exercicios_qs = exercicios_qs.filter(nome__icontains=busca_exercicio)

    # Consulta Treinos com filtro
    treinos_qs = TreinoPredefinido.objects.all()
    if busca_treino:
        treinos_qs = treinos_qs.filter(nome__icontains=busca_treino)

    # Configuração de paginação (8 itens)
    pag_exercicios = Paginator(exercicios_qs, 8)
    pag_treinos = Paginator(treinos_qs, 8)

    # Número da página corrente
    page_exercicio_number = request.GET.get('page_exercicio')
    page_treino_number = request.GET.get('page_treino')

    # Pega páginas
    exercicios_page = pag_exercicios.get_page(page_exercicio_number)
    treinos_page = pag_treinos.get_page(page_treino_number)

    # Contexto para template
    context = {
        'exercicios_page': exercicios_page,
        'treinos_page': treinos_page,
        'busca_exercicio': busca_exercicio,
        'busca_treino': busca_treino,
    }
    return render(request, 'paginas/treinos.html', context)

# Lista treinos
def pagina_treinos(request):
    exercicios = Exercicio.objects.all()
    return render(request, 'treinos.html', {'exercicios': exercicios})

# Cadastra treino
def cadastrar_treino(request, aluno_id=None):
    """
    Exibe a página de cadastro de treino para um aluno específico.
    Se aluno_id for fornecido, carrega os dados do aluno.
    """
    if aluno_id:
        aluno = get_object_or_404(Aluno, id=aluno_id)
        return render(request, 'components/rotina_form.html', {'aluno': aluno})
    else:
        return redirect('treinos')

# Cadastra exercício
def cadastrar_exercicio(request):
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        descricao = request.POST.get('descricao', '').strip()
        categoria = request.POST.get('categoria', '').strip()
        grupo_muscular = request.POST.getlist('grupo_muscular')
        
        if not nome or not categoria or not grupo_muscular:
            messages.error(request, "Preencha todos os campos obrigatórios.")
            return redirect('treinos')
        
        # Converte lista para string separada por vírgulas
        grupo_muscular_str = grupo_muscular[0] if len(grupo_muscular) == 1 else grupo_muscular[0]
        
        try:
            exercicio = Exercicio.objects.create(
                nome=nome,
                descricao=descricao,
                categoria=categoria,
                grupo_muscular=grupo_muscular_str
            )
            messages.success(request, f"Exercício '{nome}' cadastrado com sucesso.")
            
            # Retorna JSON se for uma solicitação AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'exercicio': {
                        'id': exercicio.id,
                        'nome': exercicio.nome,
                        'descricao': exercicio.descricao,
                        'categoria': exercicio.categoria,
                        'grupo_muscular': exercicio.grupo_muscular
                    }
                })
                
            return redirect('treinos')
        except Exception as e:
            messages.error(request, f"Erro ao cadastrar exercício: {str(e)}")
            return redirect('treinos')
            
    return redirect('treinos')

# View para busca AJAX de exercícios
def exercicios_json(request):
    """
    Retorna exercícios em formato JSON para busca AJAX.
    Filtra por nome se o parâmetro 'q' for fornecido.
    """
    try:
        termo = request.GET.get('q', '').strip()
        
        # Se não há termo de busca, retorna todos os exercícios (para cache inicial)
        if not termo:
            qs = Exercicio.objects.all()[:100]  # Limita a 100 para cache inicial
        else:
            # Só busca se tiver pelo menos 2 caracteres
            if len(termo) < 2:
                return JsonResponse({'results': []}, safe=False)
            
            qs = Exercicio.objects.filter(nome__icontains=termo)[:20]  # Limita a 20 resultados
        
        data = []
        for e in qs:
            # Pega o primeiro grupo muscular se houver múltiplos
            grupo_principal = e.grupo_muscular.split(',')[0] if e.grupo_muscular else ''
            
            data.append({
                'id': e.id,
                'text': e.nome,
                'nome': e.nome,
                'descricao': e.descricao or '',
                'categoria': e.categoria or '',
                'grupo_muscular': grupo_principal
            })
        
        return JsonResponse({'results': data}, safe=False)
    except Exception as e:
        return JsonResponse({
            'results': [],
            'error': str(e)
        }, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def salvar_treino(request):
    """
    Salva um treino completo com suas séries e exercícios.
    Recebe dados via JSON e cria as estruturas necessárias no banco.
    """
    try:
        dados = json.loads(request.body)
        
        # Validações básicas
        aluno_id = dados.get('aluno_id')
        if not aluno_id:
            return JsonResponse({'success': False, 'message': 'ID do aluno é obrigatório'})
        
        aluno = get_object_or_404(Aluno, id=aluno_id)
        
        series = dados.get('series', [])
        if not series:
            return JsonResponse({'success': False, 'message': 'Adicione pelo menos uma série'})
        
        # Cria um treino para cada série
        treinos_criados = []
        
        for serie_data in series:
            nome_serie = serie_data.get('nome', 'Série sem nome')
            exercicios = serie_data.get('exercicios', [])
            
            if not exercicios:
                continue  # Pula séries vazias
            
            # Cria o treino do aluno
            treino_aluno = TreinoAluno.objects.create(
                aluno=aluno,
                nome=nome_serie,
                data_inicio=date.today(),
                observacoes=dados.get('anotacoes', '')
            )
            
            # Adiciona exercícios ao treino
            for ordem, exercicio_data in enumerate(exercicios, 1):
                exercicio_id = exercicio_data.get('exercicio_id')
                if not exercicio_id:
                    continue
                    
                try:
                    exercicio = Exercicio.objects.get(id=exercicio_id)
                except Exercicio.DoesNotExist:
                    continue
                    
                TreinoAlunoExercicio.objects.create(
                    treino=treino_aluno,
                    exercicio=exercicio,
                    ordem=ordem,
                    series=exercicio_data.get('sets', 0),
                    repeticoes=exercicio_data.get('reps_desejadas', 0),
                    carga=exercicio_data.get('carga', 0),
                    intervalo_seg=exercicio_data.get('descanso', 0),
                    metodo=exercicio_data.get('metodo', ''),
                    notas=exercicio_data.get('notas', '')
                )
            
            treinos_criados.append({
                'id': treino_aluno.id,
                'nome': treino_aluno.nome,
                'exercicios_count': len(exercicios)
            })
            
            # Também cria no modelo antigo para compatibilidade
            treino_antigo = Treino.objects.create(
                aluno=aluno,
                nome=nome_serie,
                anotacoes=dados.get('anotacoes', '')
            )
            
            for ordem, exercicio_data in enumerate(exercicios, 1):
                ExercicioTreino.objects.create(
                    treino=treino_antigo,
                    nome=exercicio_data.get('nome', ''),
                    carga=exercicio_data.get('carga', 0),
                    reps=exercicio_data.get('reps_desejadas', 0),
                    desejadas=exercicio_data.get('reps_desejadas', 0),
                    sets=exercicio_data.get('sets', 0),
                    descanso=str(exercicio_data.get('descanso', 0)),
                    set1=exercicio_data.get('notas', ''),
                    ordem=ordem,
                    metodo=exercicio_data.get('metodo', ''),
                    notas=exercicio_data.get('notas', '')
                )
        
        if not treinos_criados:
            return JsonResponse({'success': False, 'message': 'Nenhuma série válida encontrada'})
        
        return JsonResponse({
            'success': True,
            'message': f'{len(treinos_criados)} treino(s) criado(s) com sucesso',
            'treinos': treinos_criados
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Dados JSON inválidos'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Erro interno: {str(e)}'})

def treinos_aluno(request, aluno_id):
    """
    Retorna o HTML da aba de treinos para um aluno específico.
    Usado para recarregar a aba após salvar um novo treino.
    """
    try:
        aluno = get_object_or_404(Aluno, id=aluno_id)
        rotinas_aluno = TreinoAluno.objects.filter(aluno=aluno).order_by('-criado_em')
        
        # Obtém exercícios para cada treino
        treinos_com_exercicios = []
        for treino in rotinas_aluno:
            exercicios = TreinoAlunoExercicio.objects.filter(treino=treino).order_by('ordem')
            treinos_com_exercicios.append({
                'treino': treino,
                'exercicios': exercicios,
                'total_exercicios': exercicios.count()
            })
        
        # Calcula estatísticas por grupo muscular
        grupos_stats = {
            'peitoral': 0,
            'costas': 0,
            'ombros': 0,
            'triceps': 0,
            'biceps': 0,
            'quadriceps': 0,
            'posterior': 0,
            'gluteo': 0,
            'panturrilha': 0
        }
        
        # Preenche estatísticas com dados reais
        for treino_info in treinos_com_exercicios:
            for exercicio in treino_info['exercicios']:
                grupo = exercicio.exercicio.grupo_muscular
                if 'chest' in grupo:
                    grupos_stats['peitoral'] += 1
                elif 'back' in grupo:
                    grupos_stats['costas'] += 1
                elif 'shoulders' in grupo:
                    grupos_stats['ombros'] += 1
                elif 'triceps' in grupo:
                    grupos_stats['triceps'] += 1
                elif 'biceps' in grupo:
                    grupos_stats['biceps'] += 1
                elif 'quadriceps' in grupo:
                    grupos_stats['quadriceps'] += 1
                elif 'hamstrings' in grupo:
                    grupos_stats['posterior'] += 1
                elif 'glutes' in grupo:
                    grupos_stats['gluteo'] += 1
                elif 'calves' in grupo:
                    grupos_stats['panturrilha'] += 1
        
        context = {
            'aluno': aluno,
            'rotinas_aluno': rotinas_aluno,
            'treinos_com_exercicios': treinos_com_exercicios,
            'treinoA_itens': TreinoAlunoExercicio.objects.filter(treino__aluno=aluno).order_by('-treino__criado_em')[:10],
            'comp': grupos_stats,
            'total_treinos': rotinas_aluno.count()
        }
        
        return render(request, 'components/aba/abaTreinos.html', context)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# API para obter exercícios de uma rotina específica
def treino_exercicios(request, treino_id):
    """
    Retorna os exercícios de um treino específico em formato JSON.
    """
    try:
        treino = get_object_or_404(TreinoAluno, id=treino_id)
        exercicios = TreinoAlunoExercicio.objects.filter(treino=treino).order_by('ordem')
        
        data = {
            'treino': {
                'id': treino.id,
                'nome': treino.nome,
                'data_inicio': treino.data_inicio.strftime('%Y-%m-%d'),
                'data_fim': treino.data_fim.strftime('%Y-%m-%d') if treino.data_fim else None,
                'observacoes': treino.observacoes
            },
            'exercicios': []
        }
        
        for ex in exercicios:
            data['exercicios'].append({
                'id': ex.id,
                'exercicio_id': ex.exercicio.id,
                'nome': ex.exercicio.nome,
                'grupo_muscular': ex.exercicio.grupo_muscular,
                'ordem': ex.ordem,
                'series': ex.series,
                'repeticoes': ex.repeticoes,
                'carga': float(ex.carga) if ex.carga else 0,
                'intervalo_seg': ex.intervalo_seg,
                'metodo': ex.metodo,
                'notas': ex.notas
            })
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Criar treino a partir de um template
@csrf_exempt
@require_http_methods(["POST"])
def criar_treino_de_template(request):
    """
    Cria um treino para um aluno a partir de um template predefinido.
    """
    try:
        dados = json.loads(request.body)
        
        aluno_id = dados.get('aluno_id')
        template_id = dados.get('template_id')
        
        if not aluno_id or not template_id:
            return JsonResponse({'success': False, 'message': 'Aluno e template são obrigatórios'})
        
        aluno = get_object_or_404(Aluno, id=aluno_id)
        template = get_object_or_404(TreinoPredefinido, id=template_id)
        
        # Cria o treino do aluno
        treino_aluno = TreinoAluno.objects.create(
            aluno=aluno,
            nome=template.nome,
            data_inicio=date.today(),
            template_origem=template,
            observacoes=template.descricao
        )
        
        # Copia os exercícios do template
        exercicios_template = TreinoPredefExercicio.objects.filter(template=template).order_by('ordem')
        
        for ex_template in exercicios_template:
            TreinoAlunoExercicio.objects.create(
                treino=treino_aluno,
                exercicio=ex_template.exercicio,
                ordem=ex_template.ordem,
                series=ex_template.series,
                repeticoes=ex_template.repeticoes,
                carga=ex_template.carga,
                intervalo_seg=ex_template.intervalo_seg,
                metodo=ex_template.metodo,
                notas=ex_template.notas
            )
        
        return JsonResponse({
            'success': True,
            'message': f'Treino "{template.nome}" criado com sucesso para {aluno.nome}',
            'treino_id': treino_aluno.id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Dados JSON inválidos'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Erro interno: {str(e)}'})