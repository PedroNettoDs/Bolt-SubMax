from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from datetime import date
from Pages.models import Aluno, Avaliacao, TreinoAluno, Plano
from .util_views import calculoGordura, calculadorMusculos, calculoGorduraKg
import json
from datetime import date
from io import BytesIO
from PIL import Image
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.core.serializers.json import DjangoJSONEncoder
from Pages.models import Aluno, Avaliacao
from .util_views import calculoGordura, calculadorMusculos
from django.contrib import messages

# Detalha aluno e exibe últimas 10 avaliações
def view_aluno(request, aluno_id):
    """Exibe os detalhes de um aluno, incluindo suas últimas 10 avaliações e rotinas de treino."""
    aluno = get_object_or_404(Aluno, id=aluno_id)
    avaliacoes = Avaliacao.objects.filter(aluno=aluno).order_by('-data')[:10]
    rotinas_aluno = TreinoAluno.objects.filter(aluno=aluno).order_by('-criado_em')
    planos = Plano.objects.all()
    
    dados_grafico = [{
        'data': a.data.strftime('%d/%m/%Y'),
        'peso': a.peso,
        'massa_muscular': a.massa_muscular,
        'gordura_percentual': a.gordura_percentual,
        'gorduraKg': a.gorduraKg,
    } for a in avaliacoes]
    
    return render(request, 'paginas/aluno_detalhe.html', {
        'aluno': aluno,
        'avaliacoes': avaliacoes,
        'rotinas_aluno': rotinas_aluno,
        'planos': planos,
        'dados_grafico_json': json.dumps(dados_grafico, cls=DjangoJSONEncoder)
    })

# Cadastra avaliação
def cadastrar_avaliacao(request, aluno_id):
    """Cadastra uma nova avaliação para o aluno especificado."""
    aluno = get_object_or_404(Aluno, id=aluno_id)
    if request.method == 'POST':
        foto = request.FILES.get('foto_avaliacao')
        numero_avaliacao = Avaliacao.objects.filter(aluno=aluno).count() + 1
        nome_arquivo = f"{aluno.id}_{aluno.nome.replace(' ', '_')}_av{numero_avaliacao}_f1.jpg"
        foto_convertida = None
        if foto:
            img = Image.open(foto).convert('RGB')
            img.thumbnail((800, 800))
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=50)
            foto_convertida = ContentFile(buffer.getvalue(), nome_arquivo)

        # Extrai dados do formulário
        peitoral = float(request.POST.get('dobra_peitoral'))
        abdominal = float(request.POST.get('dobra_abdominal'))
        coxa = float(request.POST.get('dobra_coxa'))
        triceps = float(request.POST.get('dobra_triceps'))
        subescapular = float(request.POST.get('dobra_subescapular'))
        suprailiaca = float(request.POST.get('dobra_suprailiaca'))
        axilar = float(request.POST.get('dobra_axilar'))
        altura = float(request.POST.get('altura'))
        braco = float(request.POST.get('braco_direito'))
        panturrilha = float(request.POST.get('panturrilha_direita'))
        idade = date.today().year - aluno.data_nascimento.year - ((date.today().month, date.today().day) < (aluno.data_nascimento.month, aluno.data_nascimento.day))
        sexo = aluno.sexo.lower().strip()
        peso = float(request.POST.get('peso'))
        
        gordura_percentual = calculoGordura(peitoral, abdominal, coxa, triceps, subescapular, suprailiaca, axilar, idade, sexo)
        massa_muscular = calculadorMusculos(altura, idade, sexo, braco, coxa, panturrilha, triceps, coxa, coxa)
        gordurakg = calculoGorduraKg(peitoral, abdominal, coxa, triceps, subescapular, suprailiaca, axilar, idade, sexo, peso)

        Avaliacao.objects.create(
            aluno=aluno,
            data=request.POST['data_avaliacao'],
            peso=request.POST['peso'],
            massa_muscular=massa_muscular,
            gordura_percentual=gordura_percentual,
            gorduraKg=gordurakg,
            altura=request.POST['altura'],
            peitoral=request.POST['peitoral'],
            cintura=request.POST['cintura'],
            abdomen=request.POST['abdomen'],
            quadril=request.POST['quadril'],
            braco_direito=request.POST['braco_direito'],
            braco_esquerdo=request.POST['braco_esquerdo'],
            antebraco_direito=request.POST['antebraco_direito'],
            antebraco_esquerdo=request.POST['antebraco_esquerdo'],
            coxa_direita=request.POST['coxa_direita'],
            coxa_esquerda=request.POST['coxa_esquerda'],
            panturrilha_direita=request.POST['panturrilha_direita'],
            panturrilha_esquerda=request.POST['panturrilha_esquerda'],
            dobra_peitoral=request.POST['dobra_peitoral'],
            dobra_subescapular=request.POST['dobra_subescapular'],
            dobra_axilar=request.POST['dobra_axilar'],
            dobra_triceps=request.POST['dobra_triceps'],
            dobra_abdominal=request.POST['dobra_abdominal'],
            dobra_suprailiaca=request.POST['dobra_suprailiaca'],
            dobra_coxa=request.POST['dobra_coxa'],
            postural_pescoco=request.POST['postural_pescoco'],
            postural_ombro=request.POST['postural_ombro'],
            postural_quadril=request.POST['postural_quadril'],
            postural_joelho=request.POST['postural_joelho'],
            postural_tornozelo=request.POST['postural_tornozelo'],
            observacoes=request.POST['obs'],
            foto=foto_convertida,
        )
    messages.success(request, "Avaliação Cadastrada com sucesso!.")
    return redirect('view_aluno', aluno_id=aluno.id)
    

from django.http import HttpResponse

# Atualiza uma avaliação existente
def editar_avaliacao(request, avaliacao_id):
    """Atualiza uma avaliação existente com os dados fornecidos no formulário."""
    avaliacao = get_object_or_404(Avaliacao, id=avaliacao_id)
    aluno = Aluno.objects.only('sexo', 'data_nascimento').get(id=avaliacao.aluno.id)

    peitoral = float(request.POST.get('dobra_peitoral'))
    abdominal = float(request.POST.get('dobra_abdominal'))
    coxa = float(request.POST.get('dobra_coxa'))
    triceps = float(request.POST.get('dobra_triceps'))
    subescapular = float(request.POST.get('dobra_subescapular'))
    suprailiaca = float(request.POST.get('dobra_suprailiaca'))
    axilar = float(request.POST.get('dobra_axilar'))
    altura = float(request.POST.get('altura'))
    braco = float(request.POST.get('braco_direito'))
    panturrilha = float(request.POST.get('panturrilha_direita'))
    dobra_triceps = float(request.POST.get('dobra_triceps'))
    dobra_coxa = float(request.POST.get('dobra_coxa'))
    dobra_panturrilha = float(request.POST.get('dobra_coxa'))
    peso = float(request.POST.get('peso'))

    idade = (
        date.today().year - aluno.data_nascimento.year -
        ((date.today().month, date.today().day) < (aluno.data_nascimento.month, aluno.data_nascimento.day))
    )
    sexo = str(aluno.sexo).lower().strip() if aluno.sexo else ''

    gordura_percentual = calculoGordura(peitoral, abdominal, coxa, triceps, subescapular, suprailiaca, axilar, idade, sexo)
    massa_muscular = calculadorMusculos(altura, idade, sexo, braco, coxa, panturrilha, dobra_triceps, dobra_coxa, dobra_panturrilha)
    gordurakg = calculoGorduraKg(peitoral, abdominal, coxa, triceps, subescapular, suprailiaca, axilar, idade, sexo, peso)

    if request.method == 'POST':
        avaliacao.data = request.POST.get('data_avaliacao')
        avaliacao.peso = request.POST.get('peso')
        avaliacao.massa_muscular = massa_muscular
        avaliacao.gordura_percentual = gordura_percentual
        avaliacao.gorduraKg = gordurakg
        avaliacao.observacoes = request.POST.get('obs')
        
        avaliacao.altura = request.POST.get('altura')
        avaliacao.peitoral = request.POST.get('peitoral')
        avaliacao.cintura = request.POST.get('cintura')
        avaliacao.abdomen = request.POST.get('abdomen')
        avaliacao.quadril = request.POST.get('quadril')
        avaliacao.braco_direito = request.POST.get('braco_direito')
        avaliacao.braco_esquerdo = request.POST.get('braco_esquerdo')
        avaliacao.antebraco_direito = request.POST.get('antebraco_direito')
        avaliacao.antebraco_esquerdo = request.POST.get('antebraco_esquerdo')
        avaliacao.coxa_direita = request.POST.get('coxa_direita')
        avaliacao.coxa_esquerda = request.POST.get('coxa_esquerda')
        avaliacao.panturrilha_direita = request.POST.get('panturrilha_direita')
        avaliacao.panturrilha_esquerda = request.POST.get('panturrilha_esquerda')

        avaliacao.dobra_peitoral = request.POST.get('dobra_peitoral')
        avaliacao.dobra_subescapular = request.POST.get('dobra_subescapular')
        avaliacao.dobra_axilar = request.POST.get('dobra_axilar')
        avaliacao.dobra_triceps = request.POST.get('dobra_triceps')
        avaliacao.dobra_abdominal = request.POST.get('dobra_abdominal')
        avaliacao.dobra_suprailiaca = request.POST.get('dobra_suprailiaca')
        avaliacao.dobra_coxa = request.POST.get('dobra_coxa')

        avaliacao.postural_pescoco = request.POST.get('postural_pescoco')
        avaliacao.postural_ombro = request.POST.get('postural_ombro')
        avaliacao.postural_quadril = request.POST.get('postural_quadril')
        avaliacao.postural_joelho = request.POST.get('postural_joelho')
        avaliacao.postural_tornozelo = request.POST.get('postural_tornozelo')

        
        if 'foto' in request.FILES:
            avaliacao.foto = request.FILES['foto']

        avaliacao.save()
        messages.success(request, "Avaliação editada com sucesso!")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return HttpResponse("Método não permitido", status=405)