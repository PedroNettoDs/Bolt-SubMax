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
