from django.db import models
from organizacao.models import Organizacao


class Plano(models.Model):
    """
    Planos disponíveis para alunos (mensal, trimestral, etc.)
    """
    nome = models.CharField(max_length=100)
    descricao = models.TextField()

    def __str__(self):
        return f"{self.nome} (ID: {self.id})"


class Aluno(models.Model):
    """
    Informações pessoais, médicas, preferência.
    """
    #Dados pessoais
    organizacao = models.ForeignKey(Organizacao, on_delete=models.CASCADE, null=True, blank=True)
    ativo = models.BooleanField(default=True)
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=(('M', 'Masculino'), ('F', 'Feminino')), null=True, blank=True)
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
    
    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'
        ordering = ['nome']