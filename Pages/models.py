from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from datetime import datetime, date
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from django.core.files.base import ContentFile
import os

class Organizacao(models.Model):
    """
    Modelo para representar uma organização (academia, estúdio, etc.)
    """
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=20, null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    endereco = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Plano(models.Model):
    """
    Planos disponíveis para alunos (mensal, trimestral, etc.)
    """
    nome = models.CharField(max_length=100)
    descricao = models.TextField()

    def __str__(self):
        return self.nome

class Evento(models.Model):
    """
    Eventos do calendário (aulas, reuniões, etc.)
    """
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    data = models.DateField()

    def __str__(self):
        return f"{self.titulo} - {self.data}"

class Aluno(models.Model):
    """
    Cadastro completo de alunos com informações pessoais,
    médicas, preferências e dados de treinabilidade
    """
    # Dados Pessoais
    # TODO: Adicionado campo para vincular o Aluno à sua Organização
    organizacao = models.ForeignKey('Organizacao', on_delete=models.CASCADE, null=True, blank=True)
    ativo = models.BooleanField(default=True)
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=20, null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    # Dados De Plano
    plano_status = models.BooleanField(default=True)
    plano_tipo = models.ForeignKey(Plano, on_delete=models.SET_NULL, null=True, blank=True)
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)

    # Informações Médicas
    condicoes_medicas = models.CharField(max_length=255, null=True, blank=True)
    ciclo_menstrual = models.CharField(max_length=100, null=True, blank=True)
    medicamentos = models.CharField(max_length=255, null=True, blank=True)
    lesoes = models.CharField(max_length=255, null=True, blank=True)

    # Estilo de Vida
    ocupacao = models.CharField(max_length=100, null=True, blank=True)
    estilo_vida = models.CharField(max_length=100, null=True, blank=True)
    pratica_esportes = models.CharField(max_length=100, null=True, blank=True)
    pratica_exercicios = models.CharField(max_length=100, null=True, blank=True)

    # Preferência
    dias_disponiveis = models.CharField(max_length=100, null=True, blank=True)
    horario_preferencia = models.CharField(max_length=100, null=True, blank=True)
    exercicio_preferencia = models.CharField(max_length=100, null=True, blank=True)
    info_adicional = models.CharField(max_length=255, null=True, blank=True)

    # Nível de Treinabilidade
    tempo_atual_treino = models.CharField(max_length=100, null=True, blank=True)
    tempo_destreinado = models.CharField(max_length=100, null=True, blank=True)
    tempo_treino_anterior = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.nome

class GrupoMuscular(models.Model):
    """
    Tabela imutável de músculos.
    O campo `id` armazena o identificador em inglês (ex.: 'trapezius').
    """
    id   = models.CharField(primary_key=True, max_length=20, editable=False)
    nome = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'grupo muscular'
        verbose_name_plural = 'grupos musculares'
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Exercicio(models.Model):
    """
    Tabela de exercícios principais e secundários.
    Cada exercício pode ter um grupo muscular principal e opcionalmente
    """
    nome        = models.CharField(max_length=100)
    descricao   = models.TextField(blank=True)

    # obrigatório (um só)
    grupo_muscular = models.ForeignKey(
        GrupoMuscular,
        on_delete=models.CASCADE,
        related_name='exercicios_principais',
    )

    # opcional (um só)
    grupo_muscular_secundario = models.ForeignKey(
        GrupoMuscular,
        on_delete=models.CASCADE,
        related_name='exercicios_secundarios',
        blank=True,
        null=True,
    )

# ===== MODELOS DE TREINO (NOVA ESTRUTURA) =====


class TreinoAluno(models.Model):
    """
    Treino específico atribuído a um aluno
    Pode ser baseado em um template ou criado do zero
    """
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='treinos_aluno')
    nome = models.CharField(max_length=120)
    data_inicio = models.DateField(default=date.today)
    data_fim = models.DateField(null=True, blank=True)
    observacoes = models.TextField(blank=True)
    exercicios = models.ManyToManyField(
        Exercicio,
        through='TreinoAlunoExercicio',
        related_name='treinos',
        blank=True,
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.aluno.nome}"

class TreinoAlunoExercicio(models.Model):
    """
    Tabela ponte entre TreinoAluno e Exercicio
    Define os exercícios específicos para o treino de um aluno
    com parâmetros individualizados
    """
    treino = models.ForeignKey(TreinoAluno, on_delete=models.CASCADE, related_name='exercicios')
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE)
    ordem = models.PositiveIntegerField(default=0)
    series = models.PositiveIntegerField(null=True, blank=True)
    repeticoes = models.PositiveIntegerField(null=True, blank=True)
    carga = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    intervalo_seg = models.PositiveIntegerField(null=True, blank=True)
    metodo = models.CharField(max_length=30, blank=True)
    notas = models.TextField(blank=True)

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return f"{self.exercicio.nome} ({self.treino.nome})"

# ===== MODELOS LEGADOS (MANTIDOS PARA COMPATIBILIDADE) =====

class Treino(models.Model):
    """
    Modelo legado para treinos - mantido para compatibilidade
    """
    aluno = models.ForeignKey('Aluno', on_delete=models.CASCADE, related_name='treinos')
    nome = models.CharField(max_length=50)
    anotacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.aluno.nome}"

class ExercicioTreino(models.Model):
    """
    Modelo legado para exercícios de treino - mantido para compatibilidade
    """
    treino = models.ForeignKey(Treino, on_delete=models.CASCADE, related_name='exercicios')
    nome = models.CharField(max_length=100)
    carga = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    reps = models.IntegerField(null=True, blank=True)
    desejadas = models.IntegerField(null=True, blank=True)
    descanso = models.CharField(max_length=50, blank=True)
    sets = models.IntegerField(null=True, blank=True)
    set1 = models.CharField(max_length=50, blank=True)
    ordem = models.PositiveIntegerField(default=0)
    metodo = models.CharField(max_length=30, blank=True, default='')
    notas = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nome} ({self.treino.nome})"

class SeriePersonalizada(models.Model):
    """
    Modelo legado para séries personalizadas - mantido para compatibilidade
    """
    descricao = models.CharField(max_length=50)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descricao

# ===== MODELO DE AVALIAÇÃO FÍSICA =====

class Avaliacao(models.Model):
    """
    Avaliação física completa do aluno com medidas antropométricas,
    composição corporal e avaliação postural
    """
    aluno = models.ForeignKey('Aluno', on_delete=models.CASCADE)
    data = models.DateField('Data da Avaliação')

    # Dados básicos
    peso = models.DecimalField('Peso (kg)', max_digits=9, decimal_places=2, validators=[MinValueValidator(0)])    
    massa_muscular = models.DecimalField('Massa Muscular (kg)', max_digits=9, decimal_places=2, validators=[MinValueValidator(0)], blank=True, null=True)
    gordura_percentual = models.DecimalField('Gordura (%)', max_digits=9, decimal_places=2, validators=[MinValueValidator(0)], blank=True, null=True)
    gorduraKg = models.DecimalField('Gordura (Kg)', max_digits=9, decimal_places=2, validators=[MinValueValidator(0)], blank=True, null=True)
    
    # Observações
    observacoes = models.TextField('Observações', blank=True, null=True)
    
    # Medidas antropométricas
    altura = models.DecimalField('Altura (m)', max_digits=4, decimal_places=2, validators=[MinValueValidator(0)], blank=True, null=True)
    peitoral = models.DecimalField('Peitoral (cm)', max_digits=9, decimal_places=2, blank=True, null=True)
    cintura = models.DecimalField('Cintura (cm)', max_digits=9, decimal_places=2, blank=True, null=True)
    abdomen = models.DecimalField('Abdômen (cm)', max_digits=9, decimal_places=2, blank=True, null=True)
    quadril = models.DecimalField('Quadril (cm)', max_digits=9, decimal_places=2, blank=True, null=True)

    # Membros superiores
    braco_direito = models.DecimalField('Braço Direito (cm)', max_digits=9, decimal_places=2, blank=True, null=True)
    braco_esquerdo = models.DecimalField('Braço Esquerdo (cm)', max_digits=9, decimal_places=2, blank=True, null=True)
    antebraco_direito = models.DecimalField('Antebraço Direito (cm)', max_digits=9, decimal_places=2, blank=True, null=True)
    antebraco_esquerdo = models.DecimalField('Antebraço Esquerdo (cm)', max_digits=9, decimal_places=2, blank=True, null=True)
    
    # Membros inferiores
    coxa_direita = models.DecimalField('Coxa Direita (cm)', max_digits=9, decimal_places=2, blank=True, null=True)
    coxa_esquerda = models.DecimalField('Coxa Esquerda (cm)', max_digits=9, decimal_places=2, blank=True, null=True)
    panturrilha_direita = models.DecimalField('Panturrilha Direita (cm)', max_digits=9, decimal_places=2, blank=True, null=True)
    panturrilha_esquerda = models.DecimalField('Panturrilha Esquerda (cm)', max_digits=9, decimal_places=2, blank=True, null=True)

    # Dobras cutâneas
    dobra_peitoral = models.DecimalField('Dobra Peitoral (mm)', max_digits=9, decimal_places=2, blank=True, null=True)
    dobra_subescapular = models.DecimalField('Dobra Subescapular (mm)', max_digits=9, decimal_places=2, blank=True, null=True)
    dobra_axilar = models.DecimalField('Dobra Axilar Média (mm)', max_digits=9, decimal_places=2, blank=True, null=True)
    dobra_triceps = models.DecimalField('Dobra Tríceps (mm)', max_digits=9, decimal_places=2, blank=True, null=True)
    dobra_abdominal = models.DecimalField('Dobra Abdominal (mm)', max_digits=9, decimal_places=2, blank=True, null=True)
    dobra_suprailiaca = models.DecimalField('Dobra Supra Ilíaca (mm)', max_digits=9, decimal_places=2, blank=True, null=True)
    dobra_coxa = models.DecimalField('Dobra Coxa (mm)', max_digits=9, decimal_places=2, blank=True, null=True)

    # Avaliação postural
    postural_pescoco = models.CharField('Postural Pescoço', max_length=100, blank=True)
    postural_ombro = models.CharField('Postural Ombro', max_length=100, blank=True)
    postural_quadril = models.CharField('Postural Quadril', max_length=100, blank=True)
    postural_joelho = models.CharField('Postural Joelho', max_length=100, blank=True)
    postural_tornozelo = models.CharField('Postural Tornozelo', max_length=100, blank=True)

    # Foto da avaliação
    foto = models.ImageField('Foto da Avaliação', upload_to='avaliacoes_fotos/', blank=True, null=True)

    def __str__(self):
        return f"Avaliação de {self.aluno.nome} em {self.data}"

# Modelo para armazenar informações adicionais do usuário
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    organizacao = models.ForeignKey(Organizacao, on_delete=models.SET_NULL, null=True, blank=True)
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)
    nivel_acesso = models.CharField(max_length=10, choices=[('usuario', 'Usuário'), ('admin', 'Administrador'), ('master', 'Master')], default='usuario')
    status_bloqueio = models.BooleanField(default=False)
    primeiro_acesso = models.BooleanField(default=True)

    def __str__(self):
        return self.usuario.username
