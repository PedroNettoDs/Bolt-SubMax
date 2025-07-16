import json
from datetime import date

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, render

from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action

from Pages.serializers import TreinoAlunoSerializer
from Pages.models import (Exercicio, Aluno, TreinoAluno, TreinoAluno, GrupoMuscular,)


def treinos_view(request):
    return render(request, 'paginas/treinos.html')

# API: busca exercícios com filtro opcional por nome
def exercicios_json(request):
    try:
        termo = request.GET.get('q', '').strip()

        if not termo:
            qs = Exercicio.objects.all()[:100]
        elif len(termo) >= 2:
            qs = Exercicio.objects.filter(nome__icontains=termo)[:20]
        else:
            return JsonResponse({'results': []}, safe=False)

        data = [
            {
                'id': e.id,
                'text': e.nome,
                'nome': e.nome,
                'descricao': e.descricao or '',
                'grupo_muscular': e.grupo_muscular.id if e.grupo_muscular else ''
            }
            for e in qs
        ]
        return JsonResponse({'results': data}, safe=False)

    except Exception as e:
        return JsonResponse({'results': [], 'error': str(e)}, safe=False)


# API: salvar treino completo com séries e exercícios
@csrf_exempt
@require_http_methods(["POST"])
def salvar_treino(request):
    try:
        dados = json.loads(request.body)
        aluno_id = dados.get('aluno_id')

        if not aluno_id:
            return JsonResponse({'success': False, 'message': 'ID do aluno é obrigatório'})

        aluno = get_object_or_404(Aluno, id=aluno_id)
        series = dados.get('series', [])
        if not series:
            return JsonResponse({'success': False, 'message': 'Adicione pelo menos uma série'})

        treinos_criados = []

        for serie_data in series:
            nome_serie = serie_data.get('nome', 'Série sem nome')
            exercicios = serie_data.get('exercicios', [])
            if not exercicios:
                continue

            treino_aluno = TreinoAluno.objects.create(
                aluno=aluno,
                nome=nome_serie,
                data_inicio=date.today(),
                observacoes=dados.get('anotacoes', '')
            )

            for ordem, exercicio_data in enumerate(exercicios, 1):
                exercicio_id = exercicio_data.get('exercicio_id')
                if not exercicio_id:
                    continue

                try:
                    exercicio = Exercicio.objects.get(id=exercicio_id)
                except Exercicio.DoesNotExist:
                    continue

                TreinoAluno.objects.create(
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


# API: exercícios de um treino específico
def treino_exercicios(request, treino_id):
    try:
        treino = get_object_or_404(TreinoAluno, id=treino_id)
        exercicios = TreinoAluno.objects.filter(treino=treino).order_by('ordem')

        data = {
            'treino': {
                'id': treino.id,
                'nome': treino.nome,
                'data_inicio': treino.data_inicio.strftime('%Y-%m-%d'),
                'data_fim': treino.data_fim.strftime('%Y-%m-%d') if treino.data_fim else None,
                'observacoes': treino.observacoes
            },
            'exercicios': [
                {
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
                } for ex in exercicios
            ]
        }
        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


class TreinoAlunoViewSet(viewsets.ViewSet):
    """
    Gerencia criação e visualização de treinos personalizados de alunos.
    """

    def list(self, request):
        treinos = TreinoAluno.objects.all().order_by('-criado_em')
        serializer = TreinoAlunoSerializer(treinos, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        treino = get_object_or_404(TreinoAluno, id=pk)
        serializer = TreinoAlunoSerializer(treino)
        return Response(serializer.data)

    def create(self, request):
        aluno_id = request.data.get('aluno_id')
        series = request.data.get('series', [])
        anotacoes = request.data.get('anotacoes', '')

        if not aluno_id or not series:
            return Response({'error': 'aluno_id e séries são obrigatórios.'}, status=400)

        aluno = get_object_or_404(Aluno, id=aluno_id)
        treinos_criados = []

        for serie in series:
            treino = TreinoAluno.objects.create(
                aluno=aluno,
                nome=serie.get('nome', 'Sem nome'),
                data_inicio=date.today(),
                observacoes=anotacoes
            )

            for ordem, ex in enumerate(serie.get('exercicios', []), 1):
                TreinoAluno.objects.create(
                    treino=treino,
                    exercicio_id=ex['exercicio_id'],
                    ordem=ordem,
                    series=ex.get('sets', 0),
                    repeticoes=ex.get('reps_desejadas', 0),
                    carga=ex.get('carga', 0),
                    intervalo_seg=ex.get('descanso', 0),
                    metodo=ex.get('metodo', ''),
                    notas=ex.get('notas', '')
                )

            treinos_criados.append({'id': treino.id, 'nome': treino.nome})

        return Response({'success': True, 'treinos': treinos_criados}, status=201)

    @action(detail=True, methods=['get'])
    def exercicios(self, request, pk=None):
        treino = get_object_or_404(TreinoAluno, id=pk)
        exercicios = TreinoAluno.objects.filter(treino=treino).order_by('ordem')
        data = [
            {
                'id': e.id,
                'nome': e.exercicio.nome,
                'ordem': e.ordem,
                'carga': float(e.carga),
                'series': e.series,
                'repeticoes': e.repeticoes,
                'grupo_muscular': e.exercicio.grupo_muscular.nome,
                'intervalo_seg': e.intervalo_seg,
                'metodo': e.metodo,
                'notas': e.notas,
            }
            for e in exercicios
        ]
        return Response(data)

class TreinoAlunoListCreateAPIView(generics.ListCreateAPIView):
    queryset = TreinoAluno.objects.all()
    serializer_class = TreinoAlunoSerializer

    def perform_create(self, serializer):
        # Opcional: Adicionar lógica personalizada antes de salvar, como associar o aluno logado
        # Exemplo: serializer.save(aluno=self.request.user.aluno_perfil)
        serializer.save()
