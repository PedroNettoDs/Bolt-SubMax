from django.db import models
from django.db import models
import datetime
from alunos.models import Aluno
from exercicios.models import Exercicio
from agendas.models import Agenda

class Rotina(models.Model):
    """
    Planejamento de treino contendo vários exercícios distribuídos
    ao longo da semana.
    """
    # ID Treino já é criado como AutoField (pk)
    aluno = models.ForeignKey(
        Aluno, on_delete=models.CASCADE, related_name="rotinas"
    )  # Aluno associado à rotina
    nome = models.CharField(
        max_length=120,
        help_text="Ex.: Hipertrofia Lower/Upper – 8 semanas"
    )  # Nome da rotina
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)

    # Many-to-Many via tabela de detalhes (dia, ordem, séries…)
    exercicios = models.ManyToManyField(
        Exercicio,
        through="RotinaExercicio",
        related_name="rotinas"
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    # SIMPLE RULE: data_fim ≥ data_inicio (se informado)
    def clean(self):
        super().clean()
        if self.data_fim and self.data_fim < self.data_inicio:
            raise models.ValidationError("Data fim não pode ser anterior à data início.")

    def __str__(self):
        return f"{self.nome} ({self.aluno.nome})"

    class Meta:
        verbose_name = "Rotina"
        verbose_name_plural = "Rotinas"
        ordering = ["-criado_em"]

# ------------------------------------------------------------------ #
# 2) Detalhe de cada exercício dentro da rotina
# ------------------------------------------------------------------ #
class RotinaExercicio(models.Model):
    """
    Exercício associado a uma rotina em um dia específico da semana.
    Campos de parâmetro (séries, reps…) podem ser nulos caso não se apliquem.
    """
    class DiaSemana(models.IntegerChoices):
        SEG = 0, "Segunda"
        TER = 1, "Terça"
        QUA = 2, "Quarta"
        QUI = 3, "Quinta"
        SEX = 4, "Sexta"
        SAB = 5, "Sábado"
        DOM = 6, "Domingo"

    rotina = models.ForeignKey(Rotina, on_delete=models.CASCADE, related_name="rotina_exercicios")
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE)
    dia_semana = models.PositiveSmallIntegerField(choices=DiaSemana.choices)
    ordem = models.PositiveIntegerField(default=0)

    series = models.PositiveIntegerField(null=True, blank=True)
    repeticoes = models.PositiveIntegerField(null=True, blank=True)
    carga = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    intervalo_seg = models.PositiveIntegerField(null=True, blank=True)
    notas = models.TextField(blank=True)

    class Meta:
        ordering = ["dia_semana", "ordem"]
        unique_together = ["rotina", "dia_semana", "ordem"]
        verbose_name = "Exercício da Rotina"
        verbose_name_plural = "Exercícios da Rotina"

    def __str__(self):
        return f"{self.get_dia_semana_display()} – {self.exercicio.nome}"