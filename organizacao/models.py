from django.db import models

class Organizacao(models.Model):
    """
    Modelo para representar uma Organização (academia, clínica, etc.)
    """
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=20, null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    endereco = models.TextField(null=True, blank=True)
    criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Organização'
        verbose_name_plural = 'Organizações'
        ordering = ['nome']