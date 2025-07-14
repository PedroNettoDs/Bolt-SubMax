from rest_framework import serializers
from .models import Aluno

class AlunoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Aluno.
    Inclui todos os campos do modelo Aluno.
    """
    class Meta:
        model = Aluno
        fields = '__all__' # Inclui todos os campos do modelo Aluno

from .models import Avaliacao

class AvaliacaoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Avaliacao.
    Inclui todos os campos do modelo Avaliacao.
    """
    class Meta:
        model = Avaliacao
        fields = '__all__'  # Inclui todos os campos do modelo Avaliacao

from .models import Exercicio, GrupoMuscular

class ExercicioSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Exercicio.
    Inclui todos os campos do modelo Exercicio.
    """
    grupo_muscular = serializers.SlugRelatedField(
        slug_field="id",
        queryset=GrupoMuscular.objects.all()
    )
    grupos_musculares_secundarios = serializers.SlugRelatedField(
        many=True,
        slug_field="id",
        queryset=GrupoMuscular.objects.all()
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

from .models import Organizacao

class OrganizacaoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Organizacao.
    Inclui todos os campos do modelo Organizacao.
    """
    class Meta:
        model = Organizacao
        fields = '__all__'  