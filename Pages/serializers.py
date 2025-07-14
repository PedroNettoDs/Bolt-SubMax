from rest_framework import serializers
from .models import (
    Aluno,
    Avaliacao,
    Exercicio,
    GrupoMuscular,
    Organizacao,
    Evento,
)


class AlunoSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Aluno."""

    class Meta:
        model = Aluno
        fields = "__all__"


class AvaliacaoSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Avaliacao."""

    class Meta:
        model = Avaliacao
        fields = "__all__"


class ExercicioSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Exercicio."""

    grupo_muscular = serializers.SlugRelatedField(
        slug_field="id",
        queryset=GrupoMuscular.objects.all(),
    )
    grupos_musculares_secundarios = serializers.SlugRelatedField(
        many=True,
        slug_field="id",
        queryset=GrupoMuscular.objects.all(),
    )

    class Meta:
        model = Exercicio
        fields = [
            "id",
            "nome",
            "descricao",
            "grupo_muscular",
            "grupos_musculares_secundarios",
        ]


class OrganizacaoSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Organizacao."""

    class Meta:
        model = Organizacao
        fields = "__all__"


class EventoSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Evento."""

    class Meta:
        model = Evento
        fields = ["titulo", "descricao", "data"]
