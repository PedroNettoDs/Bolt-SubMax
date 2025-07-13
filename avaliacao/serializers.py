from rest_framework import serializers
from .models import Avaliacao

class AvaliacaoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Avaliacao.
    Inclui todos os campos do modelo Avaliacao.
    """
    class Meta:
        model = Avaliacao
        fields = '__all__'  # Inclui todos os campos do modelo Avaliacao