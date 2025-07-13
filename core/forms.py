from django import forms
from alunos.models import Aluno
from exercicios.models import Exercicio
from treinos.models import Rotina
from avaliacao.models import Avaliacao


class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = '__all__'


class ExercicioForm(forms.ModelForm):
    class Meta:
        model = Exercicio
        fields = '__all__'


class RotinaForm(forms.ModelForm):
    class Meta:
        model = Rotina
        exclude = ['exercicios', 'criado_em']


class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = '__all__'
