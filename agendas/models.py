from django.db import models
from datetime import datetime
from django.utils import timezone
from alunos.models import Aluno

class Agenda(models.Model):
    """
    Agenda de compromissos / sessões de treino para um Aluno.
    """
    class Tipo(models.TextChoices):
        AVALIACAO = "AV", "Avaliação"
        TREINO    = "TR", "Treino"

    tipo = models.CharField(
        max_length=2,
        choices=Tipo.choices,
        default=Tipo.TREINO,
        help_text="AV = Avaliação mensal, TR = Sessão de treino",
        verbose_name="Tipo",
    )

    aluno = models.ForeignKey(
        Aluno, on_delete=models.CASCADE, related_name="agendas")  # Se o aluno for excluído, apaga suas agendas
    data = models.DateField()                 # Data do compromisso
    hora_inicio = models.TimeField()          # Hora de início
    hora_fim = models.TimeField()             # Hora de término
    titulo = models.CharField(max_length=100) # Resumo curto
    descricao = models.TextField(blank=True)  # Detalhes opcionais

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-data", "-hora_inicio"]
        verbose_name = "Agenda"
        verbose_name_plural = "Agendas"

    def __str__(self):
        # Exibe algo como "10/07/2025 09:00 - Treino A (João)"
        return f"{self.data} {self.hora_inicio} - {self.titulo} ({self.aluno})"
    
    # Retorna datetime pronto para o calendário
    def _dt(self, d, t):
        return timezone.make_aware(datetime.combine(d, t))

    @property
    def start_iso(self):
        return self._dt(self.data, self.hora_inicio).isoformat()

    @property
    def end_iso(self):
        return self._dt(self.data, self.hora_fim).isoformat()
    
