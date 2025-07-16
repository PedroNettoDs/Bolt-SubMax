from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from datetime import date

# ===== ORGANIZAÇÃO E USUÁRIOS =====

class Organizacao(models.Model):
    """
    Representa uma unidade (ex: academia ou estúdio)
    """
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=20, null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    endereco = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class PerfilUsuario(models.Model):
    """
    Perfil estendido do usuário (vinculado a organização)
    """
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    organizacao = models.ForeignKey(Organizacao, on_delete=models.SET_NULL, null=True, blank=True)
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)
    nivel_acesso = models.CharField(max_length=10, choices=[
        ('usuario', 'Usuário'),
        ('admin', 'Administrador'),
        ('master', 'Master'),
    ], default='usuario')
    status_bloqueio = models.BooleanField(default=False)
    primeiro_acesso = models.BooleanField(default=True)

    def __str__(self):
        return self.usuario.username

# ===== PLANOS E ALUNOS =====

class Plano(models.Model):
    """
    Plano contratado pelo aluno (ex: mensal, trimestral)
    """
    nome = models.CharField(max_length=100)
    descricao = models.TextField()

    def __str__(self):
        return self.nome

class Aluno(models.Model):
    """
    Cadastro completo de um aluno
    """
    organizacao = models.ForeignKey(Organizacao, on_delete=models.CASCADE, null=True, blank=True)
    ativo = models.BooleanField(default=True)
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=20, null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    # Plano
    plano_status = models.BooleanField(default=True)
    plano_tipo = models.ForeignKey(Plano, on_delete=models.SET_NULL, null=True, blank=True)
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)

    # Dados Médicos
    condicoes_medicas = models.CharField(max_length=255, null=True, blank=True)
    ciclo_menstrual = models.CharField(max_length=100, null=True, blank=True)
    medicamentos = models.CharField(max_length=255, null=True, blank=True)
    lesoes = models.CharField(max_length=255, null=True, blank=True)

    # Estilo de Vida
    ocupacao = models.CharField(max_length=100, null=True, blank=True)
    estilo_vida = models.CharField(max_length=100, null=True, blank=True)
    pratica_esportes = models.CharField(max_length=100, null=True, blank=True)
    pratica_exercicios = models.CharField(max_length=100, null=True, blank=True)

    # Preferências e rotina
    dias_disponiveis = models.CharField(max_length=100, null=True, blank=True)
    horario_preferencia = models.CharField(max_length=100, null=True, blank=True)
    exercicio_preferencia = models.CharField(max_length=100, null=True, blank=True)
    info_adicional = models.CharField(max_length=255, null=True, blank=True)

    # Nível de treinabilidade
    tempo_atual_treino = models.CharField(max_length=100, null=True, blank=True)
    tempo_destreinado = models.CharField(max_length=100, null=True, blank=True)
    tempo_treino_anterior = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.nome

# ===== EXERCÍCIOS =====

class GrupoMuscular(models.Model):
    """
    Grupos musculares disponíveis (id = nome técnico/slug)
    """
    id = models.CharField(primary_key=True, max_length=20, editable=False)
    nome = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'grupo muscular'
        verbose_name_plural = 'grupos musculares'
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Exercicio(models.Model):
    """
    Exercícios cadastrados no sistema
    """
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    grupo_muscular = models.ForeignKey(
        GrupoMuscular,
        on_delete=models.CASCADE,
        related_name='exercicios_principais',
    )

    grupo_muscular_secundario = models.ForeignKey(
        GrupoMuscular,
        on_delete=models.CASCADE,
        related_name='exercicios_secundarios',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.nome

# ===== TREINOS =====

class TreinoAluno(models.Model):
    """
    Treino individual e exclusivo de um aluno, com exercícios embutidos como JSON.
    Cada item da lista 'exercicios' deve conter: nome, séries, reps, carga, intervalo, método e notas.
    """
    aluno = models.ForeignKey('Aluno', on_delete=models.CASCADE, related_name='treinos')
    nome = models.CharField(max_length=120)

    # Datas principais
    data_inicio = models.DateField(default=date.today)
    data_fim = models.DateField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    observacoes = models.TextField(blank=True)

    # Lista de exercícios com parâmetros completos
    exercicios = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.nome} - {self.aluno.nome}"
    
# ===== AVALIAÇÃO FÍSICA =====

class Avaliacao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    data = models.DateField('Data da Avaliação')

    peso = models.DecimalField('Peso (kg)', max_digits=9, decimal_places=2, validators=[MinValueValidator(0)])
    massa_muscular = models.DecimalField('Massa Muscular (kg)', max_digits=9, decimal_places=2, validators=[MinValueValidator(0)], blank=True, null=True)
    gordura_percentual = models.DecimalField('Gordura (%)', max_digits=9, decimal_places=2, validators=[MinValueValidator(0)], blank=True, null=True)
    gorduraKg = models.DecimalField('Gordura (Kg)', max_digits=9, decimal_places=2, validators=[MinValueValidator(0)], blank=True, null=True)

    observacoes = models.TextField(blank=True, null=True)
    altura = models.DecimalField('Altura (m)', max_digits=4, decimal_places=2, validators=[MinValueValidator(0)], blank=True, null=True)

    # Medidas
    peitoral = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    cintura = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    abdomen = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    quadril = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)

    braco_direito = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    braco_esquerdo = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    antebraco_direito = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    antebraco_esquerdo = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    coxa_direita = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    coxa_esquerda = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    panturrilha_direita = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    panturrilha_esquerda = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)

    dobra_peitoral = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    dobra_subescapular = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    dobra_axilar = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    dobra_triceps = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    dobra_abdominal = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    dobra_suprailiaca = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    dobra_coxa = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)

    postural_pescoco = models.CharField(max_length=100, blank=True)
    postural_ombro = models.CharField(max_length=100, blank=True)
    postural_quadril = models.CharField(max_length=100, blank=True)
    postural_joelho = models.CharField(max_length=100, blank=True)
    postural_tornozelo = models.CharField(max_length=100, blank=True)

    foto = models.ImageField(upload_to='avaliacoes_fotos/', blank=True, null=True)

    def __str__(self):
        return f"Avaliação de {self.aluno.nome} em {self.data}"
    

class Evento(models.Model):
    """
    Eventos do calendário (aulas, reuniões, etc.)
    """
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    data = models.DateField()

    def __str__(self):
        return f"{self.titulo} - {self.data}"
