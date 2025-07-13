from django.db import models
from alunos.models import Aluno
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


class Avaliacao(models.Model):
    """
    Avaliação física completa do aluno com medidas antropométricas,
    composição corporal e avaliação postural
    """
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    data = models.DateField('Data da Avaliação')

    # Dados básicos
    peso = models.DecimalField('Peso (kg)', max_digits=9, decimal_places=2)    
    massa_muscular = models.DecimalField('Massa Muscular (kg)', max_digits=9, decimal_places=2, blank=True, null=True)
    gordura_percentual = models.DecimalField('Gordura (%)', max_digits=9, decimal_places=2, blank=True, null=True)
    gorduraKg = models.DecimalField('Gordura (Kg)', max_digits=9, decimal_places=2, blank=True, null=True)
    
    # Observações
    observacoes = models.TextField('Observações', blank=True, null=True)
    
    # Medidas antropométricas
    altura = models.DecimalField('Altura (m)', max_digits=4, decimal_places=2, blank=True, null=True)
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
    
    def save(self, *args, **kwargs):
        # Comprime a imagem se houver uma
        if self.foto:
            try:
                img = Image.open(self.foto)
                img = img.convert('RGB')
                img.thumbnail((800, 800))
                output = BytesIO()
                img.save(output, format='JPEG', quality=70)
                output.seek(0)
                self.foto = ContentFile(output.read(), name=self.foto.name)
            except Exception as e:
                print(f"Erro ao processar imagem: {e}")
        
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Avaliação Física'
        verbose_name_plural = 'Avaliações Físicas'
        ordering = ['-data']