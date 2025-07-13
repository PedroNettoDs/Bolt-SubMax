from rest_framework import serializers
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
