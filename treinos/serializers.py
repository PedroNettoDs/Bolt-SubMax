from rest_framework import serializers
from .models import Rotina

class treinoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Treino.
    Inclui todos os campos do modelo Treino.
    """
    class Meta:
        model = Rotina
        fields = '__all__'