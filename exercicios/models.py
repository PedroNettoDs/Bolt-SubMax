from django.db import models

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