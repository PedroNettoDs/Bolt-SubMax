from rest_framework import serializers
from .models import (
    Aluno,
    Avaliacao,
    Exercicio,
    GrupoMuscular,
    Organizacao,
    Plano,
    Evento,
    TreinoAluno,
    PerfilUsuario,
)


# ===== ALUNO E ORGANIZAÇÃO =====

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = '__all__'


class OrganizacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizacao
        fields = '__all__'


class PlanoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plano
        fields = '__all__'


class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'


class PerfilUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilUsuario
        fields = '__all__'


# ===== GRUPOS E EXERCÍCIOS =====

class GrupoMuscularSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoMuscular
        fields = '__all__'


class ExercicioSerializer(serializers.ModelSerializer):
    grupo_muscular = serializers.SlugRelatedField(
        slug_field="id",
        queryset=GrupoMuscular.objects.all()
    )
    grupo_muscular_secundario = serializers.SlugRelatedField(
        slug_field="id",
        queryset=GrupoMuscular.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Exercicio
        fields = '__all__'


# ===== TREINO ALUNO =====

class TreinoAlunoSerializer(serializers.ModelSerializer):
    """
    Serializer para TreinoAluno com campo JSON 'exercicios'.
    """
    class Meta:
        model = TreinoAluno
        fields = '__all__'


# ===== AVALIAÇÃO FÍSICA =====

class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = '__all__'
